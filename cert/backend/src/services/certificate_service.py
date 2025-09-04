import uuid
from datetime import datetime
from typing import Optional, List
from fastapi import HTTPException

from ..models.project import SeasonGroup, Project, ProjectsBySeasonResponse
from ..models.certificate import CertificateResponse, CertificateData, CertificateStatus, Role
from ..constants.error_codes import ErrorCodes, ErrorMessages, NotEligibleError
from ..utils.notion_client import NotionClient

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
        try:
            notion_client = NotionClient()
            
            # 수료증 요청 내역 생성
            certificate_request = await notion_client.create_certificate_request(certificate_data)
            
            if not certificate_request:
                raise Exception("수료증 신청 기록 생성 실패")
            
            request_id = certificate_request.get("id")
            print(f"수료증 신청 기록 생성 완료: {request_id}")
            
            # 사용자 참여 이력 확인
            participation_info = await notion_client.verify_user_participation(
                user_name=certificate_data["applicant_name"],
                course_name=certificate_data["course_name"],
                season=certificate_data["season"]
            )
            
            if not participation_info["found"]:
                raise NotEligibleError("해당 기수/스터디에서 사용자를 찾을 수 없습니다.")
            
            # TODO: pdf 수료증 생성
            # TODO: 이메일 발송
            
            # 수료증 상태 업데이트
            print("수료증 상태 업데이트")
            # TODO: 임시 값, 추후 수정 필요
            certificate_number = f"CERT-{datetime.now().strftime('%Y%m')}-{str(uuid.uuid4())[:8].upper()}" 
            
            await notion_client.update_certificate_status(
                page_id=request_id,
                status="Issued",
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
            if isinstance(e, NotEligibleError):
                # 수료 이력 없음
                print(f"수료 이력 확인 실패: {str(e)}")
                await notion_client.update_certificate_status(
                    page_id=request_id,
                    status="Not Eligible"
                )
                raise HTTPException(
                    status_code=404,
                    detail={
                        "status": "fail",
                        "error_code": ErrorCodes.NO_CERTIFICATE_HISTORY,
                        "message": str(e)
                    }
                )
            else:   
                # 시스템 오류
                print(f"시스템 오류: {e}")
                await notion_client.update_certificate_status(
                    page_id=request_id,
                    status="System Error"
                )
                # 시스템 오류
                print(f"시스템 오류: {e}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "status": "fail",
                        "error_code": ErrorCodes.PIPELINE_ERROR,
                        "message": f"{ErrorMessages.PIPELINE_ERROR}"
                    }
                )
