from pathlib import Path

from scripts.users import seed_users_from_csv
from scripts.challenge_question import seed_challenge_questions_from_csv

BASE_DIR = Path(__file__).resolve().parent


def seed_initial_data():
    """
    Seed all baseline data sets that the application depends on.
    """
    seed_users_from_csv(str(BASE_DIR / "user_data.csv"))
    seed_challenge_questions_from_csv(str(BASE_DIR / "challenge_question.csv"))
