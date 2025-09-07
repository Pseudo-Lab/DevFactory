from datetime import datetime, timedelta
import os
import aiohttp
from typing import Optional, Dict, Any, List

from ..constants.error_codes import NotEligibleError, ResponseStatus
from ..models.certificate import CertificateStatus
from ..models.project import Project, SeasonGroup, ProjectsBySeasonResponse

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
        
        self._initialized = True
    
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
                        print("data: ", data)
                        if data["results"]:
                            if len(data["results"]) > 1:
                                print(f"다 수{(len(data['results']))}의 결과가 검색되었습니다.")
                            project = data["results"][0]
                            properties = project.get("properties", {})
                            
                            # 빌더, 러너, 수료자, 이탈자 확인
                            builders = properties.get("빌더", {}).get("multi_select", [])
                            runners = properties.get("러너", {}).get("multi_select", [])
                            completers = properties.get("수료자", {}).get("rich_text", [])
                            dropouts = properties.get("이탈자", {}).get("multi_select", [])
                            
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
                                raise NotEligibleError(f"사용자 {user_name}이(가) 이탈자 목록에 있습니다.")
                            
                            # 3. 사용자가 참여자 목록에 있는지 확인
                            if user_role is None:
                                raise NotEligibleError(f"사용자 {user_name}이(가) 참여자 목록에 없습니다.")
                            
                            period = project.get("properties", {}).get("기간", {}).get("date", {})

                            if not period:
                                # TODO: 추후 처리 필요
                                raise SystemError("기간 정보가 없습니다.")

                            print(f"사용자 {user_name} 검증 성공: {user_role}")
                            return {
                                "found": True,
                                "project_id": project.get("id"),
                                "project_data": project,
                                "user_role": user_role,
                                "period": period,
                            }
                        else:
                            # 프로젝트가 검색되지 않은 경우 (Edge case)
                            print(f"프로젝트 검색 결과 없음: {user_name}, {season}기, {course_name}")
                            raise Exception("해당 프로젝트가 검색되지 않습니다. \nDevFactory로 연락부탁드립니다.")
        except Exception as e:
            print(f"사용자 참여 이력 확인 중 오류: {e}")
            return {"found": False, "user_role": None, "project_data": None, "period": None}
    
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
                    
        except Exception as e:
            print(f"수료증 신청 생성 중 오류: {e}")
            raise e
    
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
                        print(f"상태 업데이트 오류: {response.status}")
                        return False
                        
        except Exception as e:
            print(f"상태 업데이트 중 오류: {e}")
            return False

    def _get_cached_projects(self) -> Optional[List[Project]]:
        """캐시된 프로젝트 목록 가져오기"""
        cache_key = "all_projects"
        
        print(f"🔍 캐시 확인: {cache_key}")
        print(f"   - 캐시 존재: {cache_key in self._cache}")
        print(f"   - 로드 완료: {self._projects_loaded}")
        
        if cache_key in self._cache and self._projects_loaded:
            print(f"=== 캐시에서 프로젝트 로드: {len(self._cache[cache_key])}개 ===")
            return self._cache[cache_key]
        
        print("❌ 캐시 없음 - API 호출 필요")
        return None
    
    def _set_cached_projects(self, projects: List[Project]):
        """프로젝트 목록을 캐시에 저장"""
        cache_key = "all_projects"
        self._cache[cache_key] = projects
        self._cache_timestamps[cache_key] = datetime.now()
        self._projects_loaded = True  # 한 번 로드 완료
        print(f"=== 프로젝트 캐시 저장: {len(projects)}개 ===")
    
    def clear_cache(self):
        """캐시 삭제"""
        self._cache.clear()
        self._cache_timestamps.clear()
        self._projects_loaded = False
        print("=== 캐시 삭제 완료 ===")

    async def get_all_projects(self) -> Optional[list[Project]]:
        """모든 프로젝트 조회 (페이지네이션 처리 + 캐싱)"""
        # 캐시 확인
        cached_projects = self._get_cached_projects()
        if cached_projects:
            return cached_projects
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/databases/{self.databases['project_history']}/query"
                
                print("🔄 Notion API에서 프로젝트 조회 중...")
                
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
                                    
                                    project = Project(**project_data)
                                    all_projects.append(project)
                                    
                                except Exception as e:
                                    print(f"   ❌ 프로젝트 파싱 오류: {e}")
                                    print(f"   🔍 문제 데이터: {properties}")
                                    continue
                            
                            # 다음 페이지 확인
                            has_more = data.get("has_more", False)
                            start_cursor = data.get("next_cursor")
                            
                            if has_more:
                                print(f"⏭️ 다음 페이지로 이동 (cursor: {start_cursor})")
                            else:
                                print("✅ 모든 페이지 조회 완료")
                                
                        else:
                            error_text = await response.text()
                            print(f"API 오류: {response.status}")
                            print(f"오류 내용: {error_text}")
                            return None
                
                print(f"🎉 총 {len(all_projects)}개 프로젝트 조회 완료")
                
                # 캐시에 저장
                self._set_cached_projects(all_projects)
                
                return all_projects
            
        except Exception as e:
            print(f"모든 프로젝트 조회 중 오류: {e}")
            return None

    async def get_projects_by_season(self) -> Optional[ProjectsBySeasonResponse]:
        """기수별로 프로젝트 그룹화하여 조회"""
        try:
            # 모든 프로젝트 조회
            all_projects = await self.get_all_projects()
            if not all_projects:
                return None
            
            # 기수별로 그룹화
            season_groups: Dict[str, List[Project]] = {}
            
            for project in all_projects:
                season = project.season
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
            
            print(f"🎯 기수별 그룹화 완료: {len(season_list)}개 기수, {len(all_projects)}개 프로젝트")
            for season_group in season_list:
                print(f"   📊 {season_group.season}: {season_group.project_count}개 프로젝트")
            
            return response
            
        except Exception as e:
            print(f"기수별 프로젝트 조회 중 오류: {e}")
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
                        print(f"데이터베이스 구조 조회 오류: {response.status}")
                        return None
                        
        except Exception as e:
            print(f"데이터베이스 구조 조회 중 오류: {e}")
            return None
        
