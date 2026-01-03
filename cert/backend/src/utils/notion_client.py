from datetime import datetime
import json
import logging
import os
import aiohttp
from typing import Optional, Dict, Any, List

from ..constants.error_codes import NotEligibleError, ResponseStatus
from ..models.certificate import CertificateStatus
from ..models.project import Project, SeasonGroup, ProjectsBySeasonResponse


logger = logging.getLogger(__name__)

class NotionClient:
    """Notion API 클라이언트 (캐싱 포함)"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.notion_token = os.getenv("NOTION_API_KEY")
        # 데이터베이스 ID들을 환경 변수로 관리
        self.databases = {
            "project_history": os.getenv("NOTION_PROJ_DB_ID"),
            "certificate_requests": os.getenv("NOTION_CERT_DB_ID")
        }
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        # 캐시 설정
        self._cache = {}
        self._cache_timestamps = {}
        self._projects_loaded = False  # 서버 시작 후 한 번만 로드
        self.default_periods = self._load_default_periods()
        
        self._initialized = True

    def _load_default_periods(self) -> Dict[str, Dict[str, str]]:
        """시즌별 기본 기간 정보 로드"""
        env_path = os.getenv("DEFAULT_PERIODS_FILE")
        default_file_path = env_path or os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "config",
            "default_periods.json",
        )
        try:
            with open(default_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(
                "기본 기간 파일이 존재하지 않습니다.",
                extra={"path": default_file_path},
            )
        except json.JSONDecodeError:
            logger.warning(
                "기본 기간 파일 파싱에 실패했습니다.",
                extra={"path": default_file_path},
            )
        except Exception:
            logger.exception(
                "기본 기간 파일 로드 중 알 수 없는 오류가 발생했습니다.",
                extra={"path": default_file_path},
            )
        return {}
    
    async def verify_user_participation(
        self,
        user_name: str,
        course_name: str,
        season: int
    ) -> Dict[str, Any]:
        """사용자 참여 이력 확인 (빌더/러너 확인)"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/databases/{self.databases['project_history']}/query"
                
                payload = {
                    "filter": {
                        "and": [
                            {
                                "property": "기수",
                                "multi_select": {   # NOTE: select, multi_select 등 속성 값 명확하게
                                    "contains": f"{season}기"
                                }
                            },
                            {
                                "property": "이름",
                                "title": {      # NOTE: title, rich_text 은 부분 문자열 검색가능
                                    "contains": course_name
                                }
                            }
                        ]
                    }
                }
                
                async with session.post(url, headers=self.headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data["results"]:
                            if len(data["results"]) > 1:
                                logger.warning(
                                    "여러 개의 프로젝트가 검색되었습니다",
                                    extra={
                                        "result_count": len(data["results"]),
                                        "user_name": user_name,
                                        "season": season,
                                        "course_name": course_name,
                                    },
                                )
                            project = data["results"][0]
                            properties = project.get("properties", {})
                            
                            # 빌더, 러너, 수료자, 이탈자 확인
                            builders = properties.get("빌더", {}).get("multi_select", [])
                            runners = properties.get("러너", {}).get("multi_select", [])
                            completers = properties.get("수료자", {}).get("rich_text", [])
                            dropouts = properties.get("이탈자", {}).get("multi_select", [])

                            code_prop = properties.get("코드", {}).get("rich_text", [])
                            project_code = code_prop[0].get("plain_text", "") if code_prop else ""
                            if not project_code:
                                logger.warning(
                                    "프로젝트 코드가 비어 있습니다.",
                                    extra={
                                        "user_name": user_name,
                                        "season": season,
                                        "course_name": course_name,
                                        "project_id": project.get("id"),
                                    },
                                )
                            
                            builder_names = [b.get("name", "") for b in builders]
                            runner_names = [r.get("name", "") for r in runners]
                            completer_names = [c.get("plain_text", "") for c in completers]
                            dropout_names = [d.get("name", "") for d in dropouts]
                            
                            # 1. 사용자가 빌더, 러너, 수료자 중 하나에 있는지 확인
                            user_role = None
                            if user_name in builder_names:
                                user_role = "BUILDER"
                            elif user_name in runner_names:
                                user_role = "RUNNER"
                            
                            # 2. 사용자가 이탈자에 있는지 확인
                            if user_name in dropout_names:
                                raise NotEligibleError(f"수료 명단에 존재하지 않습니다. 🥲\n디스코드를 통해 질문게시판에 문의해주세요.")
                            
                            # 3. 사용자가 참여자 목록에 있는지 확인
                            if user_role is None:
                                raise NotEligibleError(f"수료 명단에 존재하지 않습니다. 🥲\n디스코드를 통해 질문게시판에 문의해주세요.")
                            
                            study_status = properties.get("단계", {}).get("select", {})
                            period_raw = project.get("properties", {}).get("기간", {}).get("date", {}) or {}

                            if not study_status:
                                raise SystemError(
                                    "스터디의 완료 정보가 없습니다.\n디스코드를 통해 질문게시판에 문의해주세요."
                                )

                            if study_status.get("name") != "완료":
                                raise NotEligibleError(
                                    "수료증은 스터디가 완료된 이후 발급 가능합니다.\n디스코드를 통해 질문게시판에 문의해주세요."
                                )

                            fallback_period = self.default_periods.get(str(season), {})
                            raw_start = period_raw.get("start")
                            raw_end = period_raw.get("end")

                            # 1) 기본값으로 초기화
                            period = {
                                "start": fallback_period.get("start"),
                                "end": fallback_period.get("end"),
                            }

                            # 2) Notion 값이 완전하면 덮어쓰기
                            if raw_start and raw_end:
                                period["start"] = raw_start
                                period["end"] = raw_end
                            # 3) 한쪽만 있을 때
                            elif raw_start or raw_end:
                                if fallback_period:
                                    logger.warning(
                                        "스터디 기간이 한쪽만 있어 기본 기간으로 대체합니다.",
                                        extra={
                                            "user_name": user_name,
                                            "season": season,
                                            "course_name": course_name,
                                            "project_id": project.get("id"),
                                            "raw_start": raw_start,
                                            "raw_end": raw_end,
                                            "fallback_start": period["start"],
                                            "fallback_end": period["end"],
                                        },
                                    )
                                else:
                                    message = (
                                        "스터디 기간 정보가 없습니다. "
                                        f"(season={season}, course={course_name}) "
                                        "config/default_periods.json의 기본 기간을 확인해주세요."
                                    )
                                    logger.error(
                                        message,
                                        extra={
                                            "user_name": user_name,
                                            "season": season,
                                            "course_name": course_name,
                                            "project_id": project.get("id"),
                                            "raw_start": raw_start,
                                            "raw_end": raw_end,
                                            "default_period_found": bool(fallback_period),
                                        },
                                    )
                                    raise SystemError(message)
                            # 4) Notion 값도 없고 기본값도 없음
                            elif not period["start"] and not period["end"]:
                                message = (
                                    "스터디 기간 정보가 없습니다. "
                                    f"(season={season}, course={course_name}) "
                                    "config/default_periods.json의 기본 기간을 확인해주세요."
                                )
                                logger.error(
                                    message,
                                    extra={
                                        "user_name": user_name,
                                        "season": season,
                                        "course_name": course_name,
                                        "project_id": project.get("id"),
                                        "default_period_found": bool(fallback_period),
                                    },
                                )
                                raise SystemError(message)

                            logger.info(
                                "사용자 검증 성공",
                                extra={
                                    "user_name": user_name,
                                    "season": season,
                                    "course_name": course_name,
                                    "user_role": user_role,
                                },
                            )
                            return {
                                "found": True,
                                "project_id": project.get("id"),
                                "project_data": project,
                                "user_role": user_role,
                                "period": period,
                                "project_code": project_code,
                            }
                        else:
                            # 프로젝트가 검색되지 않은 경우 (Edge case)
                            logger.warning(
                                "프로젝트 검색 결과 없음",
                                extra={
                                    "user_name": user_name,
                                    "season": season,
                                    "course_name": course_name,
                                },
                            )
                            raise Exception("해당 프로젝트가 검색되지 않습니다. \n디스코드를 통해 질문게시판에 문의해주세요.")
        except Exception as e:
            raise e
    
    async def create_certificate_request(
        self,   
        certificate_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """수료증 신청 기록 생성 (수료증 DB에)"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/pages"
                
                payload = {
                    "parent": {
                        "database_id": self.databases["certificate_requests"]
                    },
                    "properties": {
                        "Name": {
                            "title": [
                                {
                                    "text": {
                                        "content": certificate_data["applicant_name"]
                                    }
                                }
                            ]
                        },
                        "Issue Date": {
                            "date": {
                                "start": datetime.now().strftime("%Y-%m-%d")
                            }
                        },
                        "Recipient Email": {
                            "email": certificate_data["recipient_email"]
                        },
                        "Course Name": {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": certificate_data["course_name"]
                                    }
                                }
                            ]
                        },
                        "Season": {
                            "select": { 
                                "name": f"{certificate_data['season']}기"
                            }
                        },
                        "Certificate Status": {
                            "status": {
                                "name": CertificateStatus.PENDING
                            }
                        }
                    }
                }
                
                async with session.post(url, headers=self.headers, json=payload) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        
                        raise Exception(f"Notion API 오류 ({response.status}): {error_text}")
                    
        except Exception:
            logger.exception("수료증 신청 생성 중 오류")
            raise

    async def log_certificate_reissue(
        self,
        certificate_data: Dict[str, Any],
        certificate_number: str,
        role: str,
        issue_date: str
    ) -> Optional[Dict[str, Any]]:
        """재발급 이력 로그 생성 (수료증 DB 기록)"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/pages"

                base_properties = {
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": certificate_data["applicant_name"]
                                }
                            }
                        ]
                    },
                    "Issue Date": {
                        "date": {
                            "start": issue_date
                        }
                    },
                    "Recipient Email": {
                        "email": certificate_data["recipient_email"]
                    },
                    "Course Name": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": certificate_data["course_name"]
                                }
                            }
                        ]
                    },
                    "Season": {
                        "select": { 
                            "name": f"{certificate_data['season']}기"
                        }
                    },
                    "Certificate Number": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": certificate_number
                                }
                            }
                        ]
                    },
                    "Role": {
                        "select": {
                            "name": role
                        }
                    }
                }

                # 재발급 상태로 먼저 시도, 실패 시 기존 Issued로 폴백하여 서비스 영향 최소화
                status_candidates = [CertificateStatus.REISSUED, CertificateStatus.ISSUED]

                for status_candidate in status_candidates:
                    payload = {
                        "parent": {
                            "database_id": self.databases["certificate_requests"]
                        },
                        "properties": {
                            **base_properties,
                            "Certificate Status": {
                                "status": {
                                    "name": status_candidate
                                }
                            }
                        }
                    }

                    async with session.post(url, headers=self.headers, json=payload) as response:
                        if response.status == 200:
                            log_page = await response.json()
                            logger.info(
                                "재발급 로그 생성 완료",
                                extra={
                                    "page_id": log_page.get("id"),
                                    "certificate_number": certificate_number,
                                    "recipient_email": certificate_data.get("recipient_email"),
                                    "certificate_status": status_candidate,
                                },
                            )
                            return log_page

                        error_text = await response.text()
                        logger.warning(
                            "재발급 로그 생성 실패",
                            extra={
                                "status_code": response.status,
                                "certificate_number": certificate_number,
                                "error_text": error_text,
                                "certificate_status": status_candidate,
                            },
                        )

                return None

        except Exception:
            logger.exception("재발급 로그 생성 중 오류")
            return None
    
    async def update_certificate_status(
        self,
        page_id: str,
        status: str,
        certificate_number: str = None,
        role: str = None
    ) -> bool:
        """수료증 상태 업데이트"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/pages/{page_id}"
                
                update_data = {
                    "properties": {
                        "Certificate Status": {
                            "status": {
                                "name": status
                            }
                        }
                    }
                }
                
                # 수료증 번호 추가
                if certificate_number:
                    update_data["properties"]["Certificate Number"] = {
                        "rich_text": [
                            {
                                "text": {
                                    "content": certificate_number
                                }
                            }
                        ]
                    }
                
                # 역할 업데이트
                if role:
                    update_data["properties"]["Role"] = {
                        "select": {
                            "name": role
                        }
                    }
                
                async with session.patch(url, headers=self.headers, json=update_data) as response:
                    if response.status == 200:
                        return True
                    else:
                        logger.warning(
                            "상태 업데이트 오류",
                            extra={
                                "status_code": response.status,
                                "page_id": page_id,
                            },
                        )
                        return False
                        
        except Exception:
            logger.exception("상태 업데이트 중 오류")
            return False

    def _get_cached_projects(self) -> Optional[List[Project]]:
        """캐시된 프로젝트 목록 가져오기"""
        cache_key = "all_projects"
        
        logger.debug(
            "캐시 확인",
            extra={
                "cache_key": cache_key,
                "exists": cache_key in self._cache,
                "loaded": self._projects_loaded,
            },
        )
        
        if cache_key in self._cache and self._projects_loaded:
            logger.info(
                "캐시에서 프로젝트 로드",
                extra={"project_count": len(self._cache[cache_key])},
            )
            return self._cache[cache_key]
        
        logger.info("캐시 없음 - API 호출 예정", extra={"cache_key": cache_key})
        return None
    
    def _set_cached_projects(self, projects: List[Project]):
        """프로젝트 목록을 캐시에 저장"""
        cache_key = "all_projects"
        self._cache[cache_key] = projects
        self._cache_timestamps[cache_key] = datetime.now()
        self._projects_loaded = True  # 한 번 로드 완료
        logger.info(
            "프로젝트 캐시 저장 완료",
            extra={"project_count": len(projects)},
        )
    
    def clear_cache(self):
        """캐시 삭제"""
        self._cache.clear()
        self._cache_timestamps.clear()
        self._projects_loaded = False
        logger.info("프로젝트 캐시 삭제 완료")

    async def get_all_projects(self) -> Optional[list[Project]]:
        """모든 프로젝트 조회 (페이지네이션 처리 + 캐싱)"""
        # 캐시 확인
        cached_projects = self._get_cached_projects()
        if cached_projects:
            return cached_projects
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/databases/{self.databases['project_history']}/query"
                
                logger.info("Notion API에서 프로젝트 조회 시작")
                
                all_projects = []
                has_more = True
                start_cursor = None
                page_count = 0
                
                while has_more:
                    page_count += 1                    
                    payload = {
                        "page_size": 100,  # 최대 페이지 크기
                    }
                    
                    if start_cursor:
                        payload["start_cursor"] = start_cursor
                    
                    async with session.post(url, headers=self.headers, json=payload) as response:                        
                        if response.status == 200:
                            data = await response.json()
                            results = data.get("results", [])
                            
                            for i, result in enumerate(results):
                                try:
                                    properties = result.get("properties", {})
                                    
                                    # 안전한 데이터 추출 함수
                                    def safe_get_text(prop_name: str, default: str = "") -> str:
                                        """안전하게 텍스트 값 추출"""
                                        prop = properties.get(prop_name, {})
                                        if not prop:
                                            return default
                                        
                                        # title 타입 처리
                                        if "title" in prop:
                                            title_array = prop.get("title", [])
                                            if title_array and len(title_array) > 0:
                                                return title_array[0].get("plain_text", default)
                                        
                                        # rich_text 타입 처리
                                        if "rich_text" in prop:
                                            rich_text_array = prop.get("rich_text", [])
                                            if rich_text_array and len(rich_text_array) > 0:
                                                return rich_text_array[0].get("plain_text", default)
                                        
                                        return default
                                    
                                    # 안전하게 데이터 추출
                                    project_name = safe_get_text('이름', 'Unknown')
                                    project_description = safe_get_text('설명', '')
                                    
                                    # 기수 정보 추출
                                    season_prop = properties.get('기수', {})
                                    season = 0  # 기본값을 0으로 설정
                                    if 'multi_select' in season_prop:
                                        season_items = season_prop.get('multi_select', [])
                                        if season_items and len(season_items) > 0:
                                            season_str = season_items[0].get('name', '0기')
                                            # "10기" -> 10, "3기" -> 3
                                            try:
                                                season = int(season_str.replace('기', ''))
                                            except ValueError:
                                                season = 0  # 변환 실패시 0
                                    
                                    project_data = {
                                        "id": result.get("id", ""),
                                        "name": project_name,
                                        "description": project_description,
                                        "created_at": result.get("created_time", ""),
                                        "updated_at": result.get("last_edited_time", ""),
                                        "season": season
                                    }

                                    # 템플릿용 0기는 제외
                                    if season == 0:
                                        continue

                                    project = Project(**project_data)
                                    all_projects.append(project)
                                    
                                except Exception as e:
                                    logger.exception(
                                        "프로젝트 파싱 오류",
                                        extra={"properties": properties},
                                    )
                                    continue
                            
                            # 다음 페이지 확인
                            has_more = data.get("has_more", False)
                            start_cursor = data.get("next_cursor")
                            
                            if has_more:
                                logger.info(
                                    "다음 페이지 조회",
                                    extra={"next_cursor": start_cursor, "page": page_count},
                                )
                            else:
                                logger.info("모든 프로젝트 페이지 조회 완료")
                                
                        else:
                            error_text = await response.text()
                            logger.error(
                                "프로젝트 목록 조회 실패",
                                extra={
                                    "status_code": response.status,
                                    "error_text": error_text,
                                },
                            )
                            return None
                
                logger.info(
                    "프로젝트 조회 완료",
                    extra={"project_count": len(all_projects)},
                )
                
                # 캐시에 저장
                self._set_cached_projects(all_projects)
                
                return all_projects
            
        except Exception:
            logger.exception("모든 프로젝트 조회 중 오류")
            return None

    async def get_projects_by_season(self) -> Optional[ProjectsBySeasonResponse]:
        """기수별로 프로젝트 그룹화하여 조회"""
        try:
            # 모든 프로젝트 조회
            all_projects = await self.get_all_projects()
            if not all_projects:
                return None
            
            # 기수별로 그룹화 (템플릿용 0기는 제외)
            season_groups: Dict[str, List[Project]] = {}

            for project in all_projects:
                season = project.season
                # 템플릿용 0기는 제외
                if season == 0:
                    continue
                if season not in season_groups:
                    season_groups[season] = []
                season_groups[season].append(project)
            
            # SeasonGroup 리스트 생성
            season_list = []
            for season, projects in season_groups.items():
                season_group = SeasonGroup(
                    season=season,
                    project_count=len(projects),
                    projects=projects
                )
                season_list.append(season_group)
            
            # 기수별로 정렬 (숫자 기준)
            def sort_key(season_group: SeasonGroup) -> int:
                return season_group.season  # 이미 int이므로 그대로 사용
            
            season_list.sort(key=sort_key)
            
            # 응답 생성
            response = ProjectsBySeasonResponse(
                status=ResponseStatus.SUCCESS,
                total_projects=len(all_projects),
                total_seasons=len(season_list),
                seasons=season_list,
                message="기수별 프로젝트 조회 완료"
            )
            
            logger.info(
                "기수별 그룹화 완료",
                extra={
                    "season_count": len(season_list),
                    "project_count": len(all_projects),
                },
            )
            for season_group in season_list:
                logger.debug(
                    "기수별 프로젝트 요약",
                    extra={
                        "season": season_group.season,
                        "project_count": season_group.project_count,
                    },
                )
            
            return response
            
        except Exception:
            logger.exception("기수별 프로젝트 조회 중 오류")
            return None
                        
    async def check_existing_certificate(
        self,
        applicant_name: str,
        course_name: str,
        season: int,
        recipient_email: str = None
    ) -> Optional[Dict[str, Any]]:
        """기존 수료증 확인 (재발급용) - 이름, 코스명, 기수로 검색 (이메일 무관)"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/databases/{self.databases['certificate_requests']}/query"
                
                # 필터 조건 구성 (이름, 코스명, 기수로만 검색 - 이메일은 무관)
                filters = [
                    {
                        "property": "Name",
                        "title": {
                            "equals": applicant_name
                        }
                    },
                    {
                        "property": "Course Name",
                        "rich_text": {
                            "equals": course_name
                        }
                    },
                    {
                        "property": "Season",
                        "select": {
                            "equals": f"{season}기"
                        }
                    }
                ]
                
                payload = {
                    "filter": {
                        "and": filters
                    }
                }
                
                async with session.post(url, headers=self.headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data["results"]:
                            # 가장 최근 수료증 반환 (첫 번째 결과)
                            existing_cert = data["results"][0]
                            properties = existing_cert.get("properties", {})
                            
                            # 기존 수료증 정보 추출
                            certificate_number = ""
                            if "Certificate Number" in properties:
                                cert_num_prop = properties["Certificate Number"].get("rich_text", [])
                                if cert_num_prop:
                                    certificate_number = cert_num_prop[0].get("plain_text", "")
                            
                            role = ""
                            if "Role" in properties:
                                role_prop = properties["Role"].get("select", {})
                                if role_prop:
                                    role = role_prop.get("name", "")
                            
                            status = ""
                            if "Certificate Status" in properties:
                                status_prop = properties["Certificate Status"].get("status", {})
                                if status_prop:
                                    status = status_prop.get("name", "")
                            
                            # 이메일 정보 추출
                            existing_email = ""
                            if "Recipient Email" in properties:
                                email_prop = properties["Recipient Email"].get("email", "")
                                if email_prop:
                                    existing_email = email_prop
                            
                            logger.info(
                                "기존 수료증 발견",
                                extra={
                                    "applicant_name": applicant_name,
                                    "course_name": course_name,
                                    "season": season,
                                    "certificate_number": certificate_number,
                                    "role": role,
                                    "status": status,
                                    "existing_email": existing_email,
                                },
                            )
                            
                            return {
                                "found": True,
                                "page_id": existing_cert.get("id"),
                                "certificate_number": certificate_number,
                                "role": role,
                                "status": status,
                                "issue_date": properties.get("Issue Date", {}).get("date", {}).get("start", ""),
                                "existing_email": existing_email,
                                "existing_data": existing_cert
                            }
                        else:
                            logger.info(
                                "기존 수료증 없음",
                                extra={
                                    "applicant_name": applicant_name,
                                    "course_name": course_name,
                                    "season": season,
                                },
                            )
                            return {"found": False}
                    else:
                        error_text = await response.text()
                        logger.error(
                            "기존 수료증 확인 오류",
                            extra={
                                "status_code": response.status,
                                "error_text": error_text,
                            },
                        )
                        return None
                        
        except Exception:
            logger.exception("기존 수료증 확인 중 오류")
            return None

    async def get_certificate_by_number(self, certificate_number: str) -> Optional[Dict[str, Any]]:
        """수료증 번호로 수료증 정보 조회"""
        db_id = self.databases.get("certificate_requests")
        if not db_id:
            logger.error("수료증 데이터베이스 ID가 설정되지 않았습니다.")
            return None
            
        url = f"{self.base_url}/databases/{db_id}/query"
        payload = {
            "filter": {
                "property": "Certificate Number",
                "rich_text": {
                    "equals": certificate_number
                }
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=self.headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = data.get("results", [])
                        if results:
                            return results[0]
                        return None
                    else:
                        error_text = await response.text()
                        logger.error(f"Notion 수료증 조회 실패: {response.status}, {error_text}")
                        return None
        except Exception:
            logger.exception("Notion 수료증 조회 중 예외 발생")
            return None

    async def get_database_structure(self, database_type: str = "project_history") -> Optional[Dict[str, Any]]:
        """데이터베이스 구조 조회 (디버깅용)"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/databases/{self.databases[database_type]}"
                
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(
                            "데이터베이스 구조 조회 오류",
                            extra={"status_code": response.status, "database_type": database_type},
                        )
                        return None
                        
        except Exception:
            logger.exception("데이터베이스 구조 조회 중 오류")
            return None
        
