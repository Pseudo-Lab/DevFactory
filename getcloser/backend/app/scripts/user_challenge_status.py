import csv
from sqlalchemy.orm import Session
from core.database import SessionLocal, engine, Base
from models.challenges import UserChallengeStatus

def seed_challenges_from_csv(file_path: str):
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_challenge_status = UserChallengeStatus(
                    id=int(row["id"]),
                    user_id=int(row["user_id"]),
                    is_correct=bool(row["is_correct"]),
                    submitted_at=row["submitted_at"],
                    is_redeemed=bool(row["is_redeemed"]),
                    redeemed_at=row["redeemed_at"]
                )
                existing = db.query(UserChallengeStatus).filter_by(user_id=user_challenge_status.user_id).first()
                if not existing:
                    db.add(user_challenge_status)
        db.commit()
        print("✅ Users seeded successfully!")
    except Exception as e:
        print("❌ Error while seeding data:", e)
    finally:
        db.close()
