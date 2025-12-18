from core.database import Base, engine
from scripts.seed import seed_initial_data


def reset_database():
    """
    전체 테이블을 삭제하고 다시 생성한 후, 기본 데이터 세트를 시드합니다.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed_initial_data()
