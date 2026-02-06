import os
from pathlib import Path

from scripts.users import seed_users_from_csv
from scripts.challenge_question import seed_challenge_questions_from_csv

DEFAULT_DATA_DIR = Path(__file__).resolve().parent

# DATA_DIR 환경변수가 있으면 거기를, 없으면 기본 scripts 디렉터리를 사용
env_data_dir = os.getenv("DATA_DIR")
DATA_DIR = (
    Path(env_data_dir).expanduser().resolve()
    if env_data_dir
    else DEFAULT_DATA_DIR
)


def seed_initial_data():
    """
    Seed all baseline data sets that the application depends on.
    """
    user_csv = DATA_DIR / "user_data.csv"
    challenge_csv = DATA_DIR / "challenge_question.csv"

    for file_path in (user_csv, challenge_csv):
        if not file_path.is_file():
            raise FileNotFoundError(f"Seed file not found: {file_path}")

    seed_users_from_csv(str(user_csv))
    seed_challenge_questions_from_csv(str(challenge_csv))
