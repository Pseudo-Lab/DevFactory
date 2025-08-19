from datetime import datetime
from fastapi import APIRouter, HTTPException
from ..models.certificate import CertificateCreate, CertificateResponse
from ..services.certificate_service import CertificateService

router = APIRouter(prefix="/certs", tags=["certs"])


@router.post("/create", response_model=CertificateResponse)
async def create_certificate(certificate: CertificateCreate):
    """수료증을 생성합니다."""
    return await CertificateService.create_certificate(certificate.dict())




