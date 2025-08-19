from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    status: str = Field(..., description="성공 유무(Success/Fail)")
    message: str = Field(..., description="메시지")