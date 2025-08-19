from fastapi import APIRouter

from ..models.certificate import CertificateCreate, CertificateResponse, ErrorResponse
from ..services.certificate_service import CertificateService

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
    return await CertificateService.create_certificate(certificate.dict())




