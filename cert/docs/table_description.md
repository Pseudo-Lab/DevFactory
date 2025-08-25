# 데이터베이스 상세 구조

> (임시 테스트 시에 사용한 데이터베이스 구조)


## 수료 이력 DB 상세 구조:
총 속성 수: 42
- 1지망(선택) (rich_text)
- 모임 장소 (multi_select)
- 타입 (select)
  - 옵션: 프로젝트, 스터디, 크루, 펠로우쉽, 오픈랩, 리서치, 이니셔티브
- 추가 인원 (number)
- 기수 (multi_select)
- 이탈자 (multi_select)
- 기존 인원(팀장 포함) (number)
- 텐션 (rollup)
- 수료자 (rich_text)
- 빌더(계획표) (rollup)
- CODE (rich_text)
- 시작 인원 (rich_text)
- 3지망 (rich_text)
- 러너 (multi_select)
- 모집 인원 (rich_text)
- 단계 (select)
  - 옵션: 모집, 기획, 진행, 엔딩 프로세스, 완료, 확인 필요, 추가 활동 어려움, 폐지, 중단
- 신청 인원 (number)
- 프로젝트 계획서 (relation)
- 청강 가능 (checkbox)
- 상태 (rich_text)
- 계획표 (relation)
- 난이도 (rich_text)
- 모임 장소(계획표) (rich_text)
- 비고 (rich_text)
- 태그 (rich_text)
- 수료 기준 미달자 (rich_text)
- 현재 인원 (formula)
- 자료 공유 방법 (rich_text)
- 2지망 (rich_text)
- 모임 시간 (rich_text)
- 기간 (date)
- 디스코드 불참 (rich_text)
- 팀 페이지 (rich_text)
- 이탈자 수 (number)
- 1지망  (relation)
- 빌더 (multi_select)
- 리서치(조직) (rich_text)
- 메일 회신 (checkbox)
- 디스코드 참석 (rich_text)
- 선정 인원 (number)
- 체크 완료 (checkbox)
- 이름 (title)

## 수료증 신청 DB 상세 구조:
총 속성 수: 9
- Issue Date (date)
- Cohort (select)
  - 옵션: 10기
- Certificate Number (rich_text)
- Recipient Email (email)
- ID (unique_id)
- Certificate Status (status)
- Role (select)
  - 옵션: UNKNOWN
- Course Name (rich_text)
- Name (title)