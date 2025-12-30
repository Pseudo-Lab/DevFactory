from fastapi import APIRouter, HTTPException

from ..models.project import Project, ProjectsBySeasonResponse
from ..models.certificate import CertificateCreate, CertificateResponse, ErrorResponse
from ..services.certificate_service import CertificateService, ProjectService
from ..constants.error_codes import ResponseStatus

certificate_router = APIRouter(prefix="/certs", tags=["certs"])


@certificate_router.post(
    "/create", 
    response_model=CertificateResponse,
    responses={
        200: {
            "description": "수료증 생성 성공",
            "model": CertificateResponse
        },
        404: {
            "description": "리소스를 찾을 수 없음",
            "model": ErrorResponse
        },
        500: {
            "description": "서버 내부 오류",
            "model": ErrorResponse
        }
    }
)
async def create_certificate(certificate: CertificateCreate):
    """수료증을 생성합니다."""
    result = await CertificateService.create_certificate(certificate.dict())
    if result.status == "404":
        raise HTTPException(status_code=404, detail=result.message)
    if result.status != "200":
        # 서비스 내부 오류(템플릿/외부 연동 등)는 HTTP 500으로 전달
        raise HTTPException(status_code=500, detail=result.message)
    return result




@certificate_router.get(
    "/all-projects",
    response_model=list[Project],
    responses={
        200: {
            "description": "모든 프로젝트 조회 성공",
            "model": list[Project]
        },
        500: {
            "description": "서버 내부 오류",
            "model": ErrorResponse
        }
    }
)
async def get_all_projects():
    """모든 프로젝트 조회"""
    projects = await ProjectService.get_all_projects()
    if projects is None:
        return []  # 빈 리스트 반환
    return projects

@certificate_router.get(
    "/projects-by-season",
    response_model=ProjectsBySeasonResponse,
    responses={
        200: {
            "description": "기수별 프로젝트 조회 성공",
            "model": ProjectsBySeasonResponse
        },
        500: {
            "description": "서버 내부 오류",
            "model": ErrorResponse
        }
    }
)
async def get_projects_by_season():
    """기수별 프로젝트 조회"""
    response = await ProjectService.get_projects_by_season()
    if response is None:
        return ProjectsBySeasonResponse(
            status=ResponseStatus.ERROR,
            total_projects=0,
            total_seasons=0,
            seasons=[],
            message="프로젝트 조회 실패"
        )
    return response

@certificate_router.post("/clear-cache")
async def clear_cache():
    """캐시 삭제"""
    ProjectService.clear_cache()
    return {"message": "캐시 삭제 완료"}
