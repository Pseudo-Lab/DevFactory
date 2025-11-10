from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.challenge_schema import AnswerSubmitRequest, AnswerSubmitResponse
from services.challenge_service import submit_challenges_logic
from core.database import get_db

router = APIRouter()

@router.post("/submit-challenges", response_model=AnswerSubmitResponse)
def submit_challenges(request: AnswerSubmitRequest, db: Session = Depends(get_db)):
    try:
        is_correct = submit_challenges_logic(request.user_id, request.challenge_id, request.submitted_answer, db)
        return AnswerSubmitResponse(is_correct=is_correct)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))