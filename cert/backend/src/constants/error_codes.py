class ErrorCodes:
    """에러 코드 상수"""
    NO_CERTIFICATE_HISTORY = "CS0002"
    PIPELINE_ERROR = "CS0003"

class ErrorMessages:
    """에러 메시지 상수"""
    NO_HISTORY = "수료이력이 확인되지 않습니다. 🥲\n디스코드를 통해 김찬란에게 문의해주세요."
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
