import enum

class ProgressStatus(str, enum.Enum):
    NONE_TEAM = "NONE_TEAM"                      # 팀 없음
    TEAM_WAITING = "TEAM_WAITING"      # 팀 생성됨, 대기
    CHALLENGE_ASSIGNED = "CHALLENGE_ASSIGNED"  # 문제 할당됨
    CHALLENGE_SUCCESS = "CHALLENGE_SUCCESS"                # 문제 성공
    CHALLENGE_FAILED = "CHALLENGE_FAILED"                  # 재시도 초과
    REDEEMED = "REDEEMED"              # 굿즈 수령 완료
