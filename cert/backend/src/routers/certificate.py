from fastapi import APIRouter, HTTPException, Response, File, UploadFile

from ..models.project import Project, ProjectsBySeasonResponse
from ..models.certificate import (
    CertificateCreate,
    CertificateResponse,
    CertificateVerifyRequest,
    CertificateVerifyResponse,
    ErrorResponse,
)
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
            "model": CertificateResponse
        },
        500: {
            "description": "서버 내부 오류",
            "model": CertificateResponse
        }
    }
)
async def create_certificate(certificate: CertificateCreate, response: Response):
    """수료증을 생성합니다."""
    result = await CertificateService.create_certificate(certificate.dict())
    if result.status == "404":
        response.status_code = 404
    elif result.status != "200":
        response.status_code = 500
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

@certificate_router.post("/verify")
async def verify_certificate(file: UploadFile = File(...)):
    """수료증의 진위 여부를 확인합니다."""
    # 파일 확장자 체크 (PDF만 허용)
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="PDF 파일만 업로드 가능합니다.")
    
    try:
        file_bytes = await file.read()
        result = await CertificateService.verify_certificate(file_bytes)
        return result
    except Exception as e:
        import logging
        logging.error(f"검증 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="파일 처리 중 오류가 발생했습니다.")

@certificate_router.post(
    "/verify-by-number",
    response_model=CertificateVerifyResponse,
    responses={
        200: {
            "description": "수료증 번호 확인 성공/실패",
            "model": CertificateVerifyResponse
        },
        400: {
            "description": "잘못된 요청",
            "model": ErrorResponse
        },
        500: {
            "description": "서버 내부 오류",
            "model": ErrorResponse
        }
    }
)
async def verify_certificate_by_number(payload: CertificateVerifyRequest):
    """수료증 번호로 수료 여부를 확인합니다."""
    certificate_number = payload.certificate_number.strip()
    if not certificate_number:
        raise HTTPException(status_code=400, detail="수료증 번호를 입력해주세요.")

    result = await CertificateService.verify_certificate_by_number(certificate_number)
    return result
