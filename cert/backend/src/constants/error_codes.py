class ErrorCodes:
    """에러 코드 상수"""
    NO_CERTIFICATE_HISTORY = "CS0002"
    PIPELINE_ERROR = "CS0003"

class ErrorMessages:
    """에러 메시지 상수"""
    NO_HISTORY = "수료 명단에 존재하지 않습니다. 🥲\n입력하신 이름 '{name}'(이)가 명단에 있는지 확인하거나, 스터디 빌더 혹은 질문게시판에 문의해주세요."
    USER_DROPPED_OUT = "스터디를 수료하지 않았습니다. 🥲\n스터디 빌더 혹은 질문게시판에 문의해주세요."
    STUDY_NOT_COMPLETED = "수료증은 스터디가 완료된 이후 발급 가능합니다.\n스터디 빌더 혹은 질문게시판에 문의해주세요."
    PROJECT_NOT_FOUND = "해당 프로젝트가 검색되지 않습니다.\n기수와 스터디명을 다시 확인하거나, 스터디 빌더 혹은 질문게시판에 문의해주세요."
    PIPELINE_ERROR = "발급 처리 중 오류가 발생했습니다."
    CONTACT_INFO = "시스템 상의 오류로 수료증 발급에 실패했습니다. 🥲\n디스코드를 통해 김수현(kyopbi)에게 문의해주세요"

class ResponseStatus:
    """응답 상태 상수"""
    SUCCESS = "success"
    FAIL = "fail"
    ERROR = "error"

class NotEligibleError(Exception):
    """수료 이력이 없음"""
    def __init__(self, message: str = ErrorMessages.NO_HISTORY):
        self.message = message
        super().__init__(self.message)
