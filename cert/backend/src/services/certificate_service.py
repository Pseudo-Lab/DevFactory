import uuid
from datetime import datetime
from typing import Optional, List
from ..models.project import Project, ProjectsBySeasonResponse
from ..models.certificate import CertificateResponse, CertificateData, CertificateStatus, Role
from ..utils.notion_client import NotionClient
from ..utils.pdf_generator import PDFGenerator
from ..utils.email_sender import EmailSender
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
                print(f"기존 수료증 발견: {existing_cert.get('certificate_number')}")
                return await CertificateService._reissue_certificate(
                    certificate_data, existing_cert, notion_client
                )
            
            # 2. 신규 수료증 발급 처리
            return await CertificateService._create_new_certificate(
                certificate_data, notion_client
            )
            
        except Exception as e:
            print(f"수료증 발급 중 오류: {e}")
            return CertificateResponse(
                status="500",
                message=f"수료증 발급 중 오류가 발생했습니다: {str(e)}",
                data=None
            )
    
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
            
            print("🔄 기존 수료증 재발급 시작 (이름, 코스, 기수 일치):")
            print(f"   - 기존 수료증 번호: '{existing_cert_number}'")
            print(f"   - 요청 이메일: '{certificate_data.get('recipient_email', '')}'")
            
            # 사용자 참여 이력 재확인 (역할 정보 가져오기)
            participation_info = await notion_client.verify_user_participation(
                user_name=certificate_data["applicant_name"],
                course_name=certificate_data["course_name"],
                season=certificate_data["season"]
            )
            
            # 수료증 번호가 없는 경우 새로 생성 
            if not existing_cert_number:
                print("⚠️ 기존 수료증에 번호가 없어 새로 생성합니다.")
                existing_cert_number = f"CERT-{datetime.now().year}{participation_info['project_code']}{str(uuid.uuid4())[:2].upper()}"
                print(f"🆕 새로 생성된 수료증 번호: {existing_cert_number}")
            
            # PDF 수료증 재생성
            pdf_generator = PDFGenerator()
            pdf_bytes = pdf_generator.create_certificate(
                name=certificate_data["applicant_name"],
                season=certificate_data['season'],
                course_name=certificate_data["course_name"],
                role=participation_info["user_role"],
                period=participation_info["period"],
            )
            
            # 이메일 재발송
            email_sender = EmailSender()
            await email_sender.send_certificate_email(
                recipient_email=certificate_data["recipient_email"],
                recipient_name=certificate_data["applicant_name"],
                course_name=certificate_data["course_name"],
                season=certificate_data["season"],
                role=participation_info["user_role"],
                certificate_bytes=pdf_bytes
            )
            
            # 기존 수료증 상태를 재발급으로 업데이트
            await notion_client.update_certificate_status(
                page_id=existing_page_id,
                status=CertificateStatus.ISSUED,
                certificate_number=existing_cert_number,
                role=participation_info["user_role"]
            )
            
            print(f"수료증 재발급 완료: {existing_cert_number}")
            
            return CertificateResponse(
                status="200",
                message="기존 수료증이 재발급되었습니다.\n제출하신 이메일로 수료증이 발송되었습니다.",
                data=CertificateData(
                    id=existing_page_id,
                    name=certificate_data["applicant_name"],
                    recipient_email=certificate_data["recipient_email"],
                    certificate_number=existing_cert_number,
                    issue_date=datetime.now().strftime("%Y-%m-%d"),
                    certificate_status=CertificateStatus.ISSUED,
                    season=certificate_data["season"],
                    course_name=certificate_data["course_name"],
                    role=Role.BUILDER if participation_info["user_role"] == "BUILDER" else Role.RUNNER
                )
            )
            
        except Exception as e:
            print(f"수료증 재발급 중 오류: {e}")
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
            # print(f"수료증 신청 기록 생성 완료: {request_id}")
            
            # 사용자 참여 이력 확인
            participation_info = await notion_client.verify_user_participation(
                user_name=certificate_data["applicant_name"],
                course_name=certificate_data["course_name"],
                season=certificate_data["season"]
            )
            
            # TODO: 임시 값, 추후 수정 필요
            certificate_number = f"CERT-{datetime.now().year}{participation_info['project_code']}{str(uuid.uuid4())[:2].upper()}"

            # PDF 수료증 생성
            pdf_generator = PDFGenerator()
            pdf_bytes = pdf_generator.create_certificate(
                name=certificate_data["applicant_name"],
                season=certificate_data['season'],
                course_name=certificate_data["course_name"],
                role=participation_info["user_role"],
                period=participation_info["period"],
            )
            # 이메일 발송
            email_sender = EmailSender()
            await email_sender.send_certificate_email(
                recipient_email=certificate_data["recipient_email"],
                recipient_name=certificate_data["applicant_name"],
                course_name=certificate_data["course_name"],
                season=certificate_data["season"],
                role=participation_info["user_role"],
                certificate_bytes=pdf_bytes
            )
            
            # 수료증 상태 업데이트
            print("수료증 상태 업데이트")

            
            await notion_client.update_certificate_status(
                page_id=request_id,
                status=CertificateStatus.ISSUED,
                certificate_number=certificate_number,
                role=participation_info["user_role"]
            )
            
            print(f"수료증 발급 완료: {certificate_number}")
            
            # 5. 성공 응답 반환
            return CertificateResponse(
                status="200",
                message="제출하신 이메일로 수료증 발급이 완료되었습니다.\n메일함을 확인해보세요.",
                data=CertificateData(
                    id=request_id,
                    name=certificate_data["applicant_name"],
                    recipient_email=certificate_data["recipient_email"],
                    certificate_number=certificate_number,
                    issue_date=datetime.now().strftime("%Y-%m-%d"),
                    certificate_status=CertificateStatus.ISSUED,
                    season=certificate_data["season"],
                    course_name=certificate_data["course_name"],
                    role=Role.BUILDER if participation_info["user_role"] == "BUILDER" else Role.RUNNER
                )
            )
            
        except Exception as e:
            # 시스템 오류
            print(f"신규 수료증 발급 중 시스템 오류: {e}")
            if request_id:  # request_id가 존재하는 경우에만 상태 업데이트
                await notion_client.update_certificate_status(
                    page_id=request_id,
                    status=CertificateStatus.SYSTEM_ERROR
                )
            raise e