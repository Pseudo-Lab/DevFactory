from pydantic import BaseModel, Field
from enum import Enum

class CertificateStatus(str, Enum):
    """수료증 상태"""
    PENDING = "대기중"
    ISSUED = "발급 완료"
    FAILED = "발급 실패"

class Role(str, Enum):
    """역할 구분"""
    BUILDER = "빌더"
    RUNNER = "러너"

class CertificateCreate(BaseModel):
    """수료증 생성 요청 모델"""
    applicant_name: str = Field(..., description="신청자 이름", example="홍길동")
    recipient_email: str = Field(..., description="수료자 이메일", example="hong@example.com")
    course_name: str = Field(..., description="스터디명", example="Wrapping Up Pseudolab" )
    season: int = Field(..., description="활동기수 (ex. 10)", example=10)

class CertificateData(BaseModel):
    """수료증 데이터 모델 (Notion DB 구조 기반)"""
    id: str = Field(..., example="2533a2a2-eed5-81fa-9921-c14d2cd117b7", description="수료증 신청 페이지 ID")
    name: str = Field(..., example="홍길동", description="신청자 이름")
    recipient_email: str = Field(..., example="hong@example.com", description="수료자 이메일")
    certificate_number: str = Field(..., example="CERT-2024-001", description="수료증 번호")
    issue_date: str = Field(..., example="2024-01-15", description="신청 날짜")
    certificate_status: CertificateStatus = Field(..., example=CertificateStatus.PENDING, description="발급 여부")
    season: int = Field(..., example=10, description="참여 기수")
    course_name: str = Field(..., example="Wrapping Up Pseudolab", description="스터디명")
    role: Role = Field(..., example=Role.BUILDER, description="빌더/러너 구분")

class CertificateResponse(BaseModel):
    """수료증 응답 모델"""
    status: str = Field(..., example="success", description="응답 상태")
    message: str = Field(..., example="수료증이 성공적으로 생성되었습니다.", description="응답 메시지")
    data: CertificateData = Field(..., description="수료증 데이터")


class ErrorResponse(BaseModel):
    """에러 응답 모델"""
    status: str = Field(..., example="fail", description="응답 상태")
    error_code: str = Field(..., example="CS0002", description="에러 코드")
    message: str = Field(..., example="수료이력이 확인되지 않습니다.", description="에러 메시지")