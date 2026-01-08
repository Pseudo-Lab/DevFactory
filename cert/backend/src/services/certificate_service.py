import logging
import uuid
import re
from datetime import datetime
from typing import Optional, List

from ..constants.error_codes import NotEligibleError
from ..models.project import Project, ProjectsBySeasonResponse
from ..models.certificate import CertificateResponse, CertificateData, CertificateStatus, Role
from ..utils.notion_client import NotionClient
from ..utils.pdf_generator import PDFGenerator
from ..utils.email_sender import EmailSender


logger = logging.getLogger(__name__)
class ProjectService:
    """프로젝트 서비스"""

    @staticmethod
    async def get_all_projects() -> Optional[List[Project]]:
        """모든 프로젝트 조회"""
        notion_client = NotionClient()
        return await notion_client.get_all_projects()
    
    @staticmethod
    async def get_projects_by_season() -> Optional[ProjectsBySeasonResponse]:
        """기수별 프로젝트 조회"""
        notion_client = NotionClient()
        return await notion_client.get_projects_by_season()
    
    @staticmethod
    def clear_cache():
        """캐시 삭제"""
        notion_client = NotionClient()
        notion_client.clear_cache()
    
class CertificateService:
    """수료증 서비스"""    

    @staticmethod
    def _get_study_year(period: dict) -> int:
        """스터디 기간에서 연도를 추출 (없으면 현재 연도 fallback)"""
        for key in ("start", "end"):
            raw_date = (period or {}).get(key)
            if raw_date:
                try:
                    return datetime.fromisoformat(raw_date).year
                except ValueError:
                    # ISO 포맷이 아니면 연도만 파싱 시도
                    year_part = raw_date.split("-", 1)[0]
                    if year_part.isdigit():
                        return int(year_part)
        return datetime.now().year

    @staticmethod
    def _build_certificate_number(
        study_year: int,
        unique_identifier: str,
        track_code: str,
        season_code: str,
        study_id: str,
    ) -> str:
        """수료증 번호 생성: {코드}{연도}{기수}-{스터디ID}{unique_id}"""
        suffix = f"{study_id}{unique_identifier.upper()}"
        return f"{track_code}{study_year}{season_code}-{suffix}"

    @staticmethod
    def _parse_project_code(project_code: str, season: int) -> tuple[str | None, str, str | None]:
        """프로젝트 코드 파싱: CODE에서 트랙/기수/스터디ID 추출"""
        track_code = None
        season_code = f"S{season:02d}"
        study_id = None

        if not project_code:
            return track_code, season_code, study_id

        raw_code = project_code.strip()
        if "-" in raw_code:
            parts = raw_code.split("-", 1)
        elif "_" in raw_code:
            parts = raw_code.split("_", 1)
        else:
            parts = [raw_code]

        if parts:
            season_match = re.match(r"^S(\d+)$", parts[0], re.IGNORECASE)
            if season_match:
                season_code = f"S{int(season_match.group(1)):02d}"

        target = parts[1] if len(parts) > 1 else raw_code
        match = re.match(r"^([A-Za-z]+)(\d+)$", target)
        if match:
            track_code = match.group(1).upper()
            study_id = match.group(2)

        return track_code, season_code, study_id
    
    @staticmethod
    async def create_certificate(certificate_data: dict) -> CertificateResponse:
        """수료증 생성 및 발급
        
        Args:
            certificate_data: 수료증 생성 데이터
            
        Returns:
            수료증 생성 결과
            
        """
        notion_client = NotionClient()
        
        try:
            # 1. 기존 수료증 확인 (재발급 여부 판단)
            existing_cert = await notion_client.check_existing_certificate(
                applicant_name=certificate_data["applicant_name"],
                course_name=certificate_data["course_name"],
                season=certificate_data["season"],
                recipient_email=certificate_data.get("recipient_email")
            )
            
            # 기존 수료증 확인이 성공하고 기존 수료증이 있는 경우 재발급 처리
            if existing_cert and existing_cert.get("found"):
                existing_status = existing_cert.get("status", "")
                if existing_status in [CertificateStatus.ISSUED, CertificateStatus.REISSUED]:
                    logger.info(
                        "기존 수료증 발견 (재발급 진행)",
                        extra={
                            "certificate_number": existing_cert.get("certificate_number"),
                            "applicant_name": certificate_data.get("applicant_name"),
                            "season": certificate_data.get("season"),
                            "status": existing_status,
                        },
                    )
                    return await CertificateService._reissue_certificate(
                        certificate_data, existing_cert, notion_client
                    )

                logger.info(
                    "기존 수료증 발견했지만 상태가 Issued/Reissued가 아님. 신규 발급으로 진행",
                    extra={
                        "certificate_number": existing_cert.get("certificate_number"),
                        "applicant_name": certificate_data.get("applicant_name"),
                        "season": certificate_data.get("season"),
                        "status": existing_status,
                    },
                )
            
            # 2. 신규 수료증 발급 처리
            return await CertificateService._create_new_certificate(
                certificate_data, notion_client
            )
            
        except NotEligibleError as e:
            logger.warning(
                "수료 이력 없음",
                extra={
                    "applicant_name": certificate_data.get("applicant_name"),
                    "season": certificate_data.get("season"),
                    "course_name": certificate_data.get("course_name"),
                },
            )
            return CertificateResponse(
                status="404",
                message=e.message,
                data=None,
            )
        except Exception as e:
            logger.exception("수료증 발급 중 오류")
            return CertificateResponse(
                status="500",
                message="수료증 발급을 완료하지 못했습니다. 관리자에게 문의해주세요.",
                data=None,
            )

    @staticmethod
    async def verify_certificate(file_bytes: bytes) -> dict:
        """수료증 검증"""
        try:
            pdf_generator = PDFGenerator()
            watermark_text = pdf_generator.extract_watermark_from_pdf(file_bytes)
            
            if not watermark_text:
                return {
                    "valid": False,
                    "message": "수료증에서 워터마크를 찾을 수 없습니다."
                }
                
            # 기본 검증 (PSEUDOLAB 접두사 확인)
            if not watermark_text.startswith("PSEUDOLAB"):
                return {
                    "valid": False,
                    "message": "유효하지 않은 수료증 워터마크입니다.",
                    "debug_text": watermark_text
                }
                
            # 수료증 번호 추출 (A2025S10-0156 포맷 기대)
            cert_number = ""
            if "_" in watermark_text:
                cert_number = watermark_text.split("_")[1]
            
            # 번호가 없는 경우 (테스트용 등)
            if not cert_number:
                return {
                    "valid": True,
                    "message": "워터마크가 확인되었습니다 (테스트용/번호없음).",
                    "watermark_text": watermark_text
                }

            # Notion 실데이터 조회
            notion_client = NotionClient()
            cert_page = await notion_client.get_certificate_by_number(cert_number)
            
            if not cert_page:
                return {
                    "valid": False,
                    "message": f"수료증 번호({cert_number})에 해당하는 발급 기록을 찾을 수 없습니다."
                }
            return CertificateService._build_verification_result(cert_page, cert_number)
            
        except Exception as e:
            if "워터마크를 찾을 수 없습니다" in str(e):
                logger.info(f"수료증 검증 실패 (워터마크 없음): {str(e)}")
            else:
                logger.exception("수료증 검증 중 예상치 못한 오류")
            return {
                "valid": False,
                "message": "수료증 검증 처리 중 오류가 발생했습니다."
            }

    @staticmethod
    async def verify_certificate_by_number(certificate_number: str) -> dict:
        """수료증 번호로 수료 여부 확인"""
        try:
            notion_client = NotionClient()
            cert_page = await notion_client.get_certificate_by_number(certificate_number)

            if not cert_page:
                return {
                    "valid": False,
                    "message": f"수료증 번호({certificate_number})에 해당하는 발급 기록을 찾을 수 없습니다."
                }

            return CertificateService._build_verification_result(cert_page, certificate_number)
        except Exception:
            logger.exception("수료증 번호 확인 중 오류")
            return {
                "valid": False,
                "message": "수료증 번호 확인 처리 중 오류가 발생했습니다."
            }

    @staticmethod
    def _build_verification_result(cert_page: dict, certificate_number: str) -> dict:
        """Notion 수료증 페이지 응답 포맷팅"""
        props = cert_page.get("properties", {})

        name = props.get("Name", {}).get("title", [{}])[0].get("plain_text", "알 수 없음")
        course = props.get("Course Name", {}).get("rich_text", [{}])[0].get("plain_text", "알 수 없음")
        season = props.get("Season", {}).get("select", {}).get("name", "알 수 없음")
        issue_date = props.get("Issue Date", {}).get("date", {}).get("start", "알 수 없음")
        status = props.get("Certificate Status", {}).get("status", {}).get("name", "알 수 없음")

        return {
            "valid": True,
            "message": "수료증 확인에 성공했습니다.",
            "data": {
                "name": name,
                "course": course,
                "season": season,
                "issue_date": issue_date
            }
        }
    
    @staticmethod
    async def _reissue_certificate(
        certificate_data: dict, 
        existing_cert: dict, 
        notion_client: NotionClient
    ) -> CertificateResponse:
        """기존 수료증 재발급"""
        try:
            # 기존 수료증 정보 사용
            existing_page_id = existing_cert.get("page_id")
            existing_cert_number = existing_cert.get("certificate_number")
            
            logger.info(
                "기존 수료증 재발급 시작",
                extra={
                    "existing_certificate_number": existing_cert_number,
                    "recipient_email": certificate_data.get("recipient_email", ""),
                    "applicant_name": certificate_data.get("applicant_name"),
                    "season": certificate_data.get("season"),
                },
            )
            
            # 사용자 참여 이력 재확인 (역할 정보 가져오기)
            participation_info = await notion_client.verify_user_participation(
                user_name=certificate_data["applicant_name"],
                course_name=certificate_data["course_name"],
                season=certificate_data["season"]
            )
            
            # 수료증 번호가 없는 경우 새로 생성 
            if not existing_cert_number:
                logger.warning(
                    "기존 수료증 번호 없음. 새로 생성",
                    extra={"applicant_name": certificate_data["applicant_name"]},
                )
                # 기존 수료증 번호가 없으면 DB ID(Unique ID) 기반으로 생성
                existing_data = existing_cert.get("existing_data", {})
                properties = existing_data.get("properties", {})
                
                # 로그에서 확인된 구조: properties['ID']['unique_id']['number']
                id_prop = properties.get("ID", {})
                unique_identifier = None
                
                if id_prop.get("type") == "unique_id":
                    unique_identifier = str(id_prop.get("unique_id", {}).get("number"))
                
                if not unique_identifier:
                    # fallback: 혹시 ID 컬럼명이 다를 경우를 대비해 기존 방식 유지
                    for prop_val in properties.values():
                        if prop_val.get("type") == "unique_id":
                            unique_identifier = str(prop_val.get("unique_id", {}).get("number"))
                            break

                
                study_year = CertificateService._get_study_year(participation_info.get("period", {}))
                track_code, season_code, study_id = CertificateService._parse_project_code(
                    participation_info.get("project_code", ""),
                    certificate_data["season"],
                )
                if not track_code:
                    track_code = "N"
                if not study_id:
                    study_index = await notion_client.get_study_order_index(
                        season=certificate_data["season"],
                        course_name=certificate_data["course_name"],
                    )
                    if study_index is None:
                        message = "스터디 순서를 확인할 수 없어 수료증을 발급할 수 없습니다."
                        logger.error(
                            message,
                            extra={
                                "season": certificate_data["season"],
                                "course_name": certificate_data["course_name"],
                            },
                        )
                        raise Exception(message)
                    else:
                        study_id = f"{study_index:02d}" if study_index < 100 else str(study_index)

                existing_cert_number = CertificateService._build_certificate_number(
                    study_year=study_year,
                    unique_identifier=unique_identifier,
                    track_code=track_code,
                    season_code=season_code,
                    study_id=study_id,
                )
                logger.info(
                    "새로운 수료증 번호 생성",
                    extra={"certificate_number": existing_cert_number},
                )
            
            # 발급일(재발급 시점 기준)
            issue_date = datetime.now().strftime("%Y-%m-%d")

            # PDF 수료증 재생성
            pdf_generator = PDFGenerator()
            pdf_bytes = pdf_generator.create_certificate(
                name=certificate_data["applicant_name"],
                season=certificate_data['season'],
                course_name=certificate_data["course_name"],
                role=participation_info["user_role"],
                period=participation_info["period"],
                certificate_number=existing_cert_number,
                issue_date=issue_date,
            )
            
            # 이메일 재발송
            email_sender = EmailSender()
            email_sent = await email_sender.send_certificate_email(
                recipient_email=certificate_data["recipient_email"],
                recipient_name=certificate_data["applicant_name"],
                course_name=certificate_data["course_name"],
                season=certificate_data["season"],
                role=participation_info["user_role"],
                certificate_bytes=pdf_bytes
            )
            
            if not email_sent:
                raise Exception("재발급 이메일 발송 실패")

            # 재발급 로그 기록
            reissue_log = await notion_client.log_certificate_reissue(
                certificate_data=certificate_data,
                certificate_number=existing_cert_number,
                role=participation_info["user_role"],
                issue_date=issue_date
            )
            if not reissue_log:
                logger.warning(
                    "재발급 로그 기록 실패",
                    extra={
                        "certificate_number": existing_cert_number,
                        "recipient_email": certificate_data["recipient_email"],
                    },
                )
            
            # 기존 수료증 상태를 재발급으로 업데이트
            await notion_client.update_certificate_status(
                page_id=existing_page_id,
                status=CertificateStatus.ISSUED,
                certificate_number=existing_cert_number,
                role=participation_info["user_role"]
            )
            
            logger.info(
                "수료증 재발급 완료",
                extra={
                    "certificate_number": existing_cert_number,
                    "recipient_email": certificate_data["recipient_email"],
                },
            )
            
            return CertificateResponse(
                status="200",
                message="기존 수료증이 재발급되었습니다.\n제출하신 이메일로 수료증이 발송되었습니다.",
                data=CertificateData(
                    id=existing_page_id,
                    name=certificate_data["applicant_name"],
                    recipient_email=certificate_data["recipient_email"],
                    certificate_number=existing_cert_number,
                    issue_date=issue_date,
                    certificate_status=CertificateStatus.ISSUED,
                    season=certificate_data["season"],
                    course_name=certificate_data["course_name"],
                    role=Role.BUILDER if participation_info["user_role"] == "BUILDER" else Role.RUNNER
                )
            )
            
        except Exception as e:
            logger.exception("수료증 재발급 중 오류")
            raise e
    
    @staticmethod
    async def _create_new_certificate(
        certificate_data: dict, 
        notion_client: NotionClient
    ) -> CertificateResponse:
        """신규 수료증 발급"""
        request_id = None
        try:
            # 수료증 요청 내역 생성
            certificate_request = await notion_client.create_certificate_request(certificate_data)
            
            if not certificate_request:
                raise Exception("수료증 신청 기록 생성 실패")
            
            request_id = certificate_request.get("id")
            logger.info(
                "수료증 신청 기록 생성 완료",
                extra={"request_id": request_id, "recipient_email": certificate_data.get("recipient_email")},
            )
            
            # 사용자 참여 이력 확인
            participation_info = await notion_client.verify_user_participation(
                user_name=certificate_data["applicant_name"],
                course_name=certificate_data["course_name"],
                season=certificate_data["season"]
            )
            
            # DB ID(Unique ID)를 사용하여 수료증 번호 생성
            properties = certificate_request.get("properties", {})
            unique_identifier = None
            
            # 로그에서 확인된 구조: properties['ID']['unique_id']['number']
            id_prop = properties.get("ID", {})
            if id_prop.get("type") == "unique_id":
                unique_identifier = str(id_prop.get("unique_id", {}).get("number"))

            if not unique_identifier:
                 # fallback: 혹시 ID 컬럼명이 다를 경우를 대비해 순회 검색
                for prop_val in properties.values():
                    if prop_val.get("type") == "unique_id":
                        unique_identifier = str(prop_val.get("unique_id", {}).get("number"))
                        break
            
            if not unique_identifier:
                # fallback: Page ID의 마지막 5자리
                unique_identifier = request_id.replace("-", "")[-5:]

            study_year = CertificateService._get_study_year(participation_info.get("period", {}))
            track_code, season_code, study_id = CertificateService._parse_project_code(
                participation_info.get("project_code", ""),
                certificate_data["season"],
            )
            if not track_code:
                track_code = "N"
            if not study_id:
                study_index = await notion_client.get_study_order_index(
                    season=certificate_data["season"],
                    course_name=certificate_data["course_name"],
                )
                if study_index is None:
                    message = "스터디 순서를 확인할 수 없어 수료증을 발급할 수 없습니다."
                    logger.error(
                        message,
                        extra={
                            "season": certificate_data["season"],
                            "course_name": certificate_data["course_name"],
                        },
                    )
                    raise Exception(message)
                else:
                    study_id = f"{study_index:02d}" if study_index < 100 else str(study_index)

            certificate_number = CertificateService._build_certificate_number(
                study_year=study_year,
                unique_identifier=unique_identifier,
                track_code=track_code,
                season_code=season_code,
                study_id=study_id,
            )
            issue_date = datetime.now().strftime("%Y-%m-%d")

            # PDF 수료증 생성
            pdf_generator = PDFGenerator()
            pdf_bytes = pdf_generator.create_certificate(
                name=certificate_data["applicant_name"],
                season=certificate_data['season'],
                course_name=certificate_data["course_name"],
                role=participation_info["user_role"],
                period=participation_info["period"],
                certificate_number=certificate_number,
                issue_date=issue_date,
            )
            # 이메일 발송
            email_sender = EmailSender()
            email_sent = await email_sender.send_certificate_email(
                recipient_email=certificate_data["recipient_email"],
                recipient_name=certificate_data["applicant_name"],
                course_name=certificate_data["course_name"],
                season=certificate_data["season"],
                role=participation_info["user_role"],
                certificate_bytes=pdf_bytes
            )

            if not email_sent:
                raise Exception("이메일 발송 실패")
            
            # 수료증 상태 업데이트
            logger.info(
                "수료증 상태 업데이트",
                extra={
                    "request_id": request_id,
                    "certificate_number": certificate_number,
                },
            )

            
            await notion_client.update_certificate_status(
                page_id=request_id,
                status=CertificateStatus.ISSUED,
                certificate_number=certificate_number,
                role=participation_info["user_role"]
            )
            
            logger.info(
                "수료증 발급 완료",
                extra={
                    "certificate_number": certificate_number,
                    "recipient_email": certificate_data["recipient_email"],
                },
            )
            
            # 5. 성공 응답 반환
            return CertificateResponse(
                status="200",
                message="제출하신 이메일로 수료증 발급이 완료되었습니다.\n메일함을 확인해보세요.",
                data=CertificateData(
                    id=request_id,
                    name=certificate_data["applicant_name"],
                    recipient_email=certificate_data["recipient_email"],
                    certificate_number=certificate_number,
                    issue_date=issue_date,
                    certificate_status=CertificateStatus.ISSUED,
                    season=certificate_data["season"],
                    course_name=certificate_data["course_name"],
                    role=Role.BUILDER if participation_info["user_role"] == "BUILDER" else Role.RUNNER
                )
            )
            
        except Exception as e:
            # 시스템 오류
            logger.exception("신규 수료증 발급 중 시스템 오류")
            if request_id:  # request_id가 존재하는 경우에만 상태 업데이트
                await notion_client.update_certificate_status(
                    page_id=request_id,
                    status=CertificateStatus.SYSTEM_ERROR
                )
            raise e
