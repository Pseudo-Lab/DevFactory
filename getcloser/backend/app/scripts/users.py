import csv
from sqlalchemy.orm import Session
from core.database import SessionLocal, engine, Base
from models.users import User

def seed_users_from_csv(file_path: str):
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user = User(
                    id=int(row["user_id"]),
                    email=row["email"],
                    name=row["name"]
                )
                existing = db.query(User).filter_by(email=user.email).first()
                if not existing:
                    db.add(user)
        db.commit()
        print("✅ Users seeded successfully!")
    except Exception as e:
        print("❌ Error while seeding data:", e)
    finally:
        db.close()

# if __name__ == "__main__":
#     seed_users_from_csv("user_data.csv")
