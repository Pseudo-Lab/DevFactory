from pydantic import BaseModel, Field
from typing import List, Dict, Any

from ..models.core import BaseResponse

class Project(BaseModel):
    id: str = Field(..., example="2533a2a2-eed5-81fa-9921-c14d2cd117b7", description="프로젝트 ID")
    name: str = Field(..., example="프로젝트 이름", description="프로젝트 이름")
    season: int = Field(..., example=10, description="기수")
    description: str = Field(..., example="프로젝트 설명", description="프로젝트 설명")
    created_at: str = Field(..., example="2025-08-18", description="프로젝트 생성 일자")
    updated_at: str = Field(..., example="2025-08-18", description="프로젝트 수정 일자")

class SeasonGroup(BaseModel):
    """기수별 프로젝트 그룹"""
    season: int = Field(..., example=10, description="기수")
    project_count: int = Field(..., example=25, description="해당 기수의 프로젝트 수")
    projects: List[Project] = Field(..., description="해당 기수의 프로젝트 목록")

class ProjectsBySeasonResponse(BaseResponse):
    """기수별 프로젝트 응답 모델"""
    total_projects: int = Field(..., example=150, description="전체 프로젝트 수")
    total_seasons: int = Field(..., example=6, description="전체 기수 수")
    seasons: List[SeasonGroup] = Field(..., description="기수별 프로젝트 그룹 목록")