import csv
from sqlalchemy.orm import Session
from core.database import SessionLocal, engine, Base
from models.challenge_question import ChallengeQuestion

def seed_challenge_questions_from_csv(file_path: str):
    # 테이블 생성 (없으면)
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                challenge = ChallengeQuestion(
                    id=int(row["id"]),
                    user_id=int(row["user_id"]),
                    category=row["category"],
                    answer=row["answer"]
                )
                # 이미 같은 challenge_id가 있는지 확인
                existing = db.query(ChallengeQuestion).filter_by(id=challenge.id).first()
                if not existing:
                    db.add(challenge)

        db.commit()
        print("✅ Challenge questions seeded successfully!")

    except Exception as e:
        print("❌ Error while seeding data:", e)

    finally:
        db.close()


# if __name__ == "__main__":
#     seed_challenge_questions_from_csv("./scripts/challenge_question.csv")
