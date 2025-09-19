import os
from typing import Tuple

class TemplateContent:
    """템플릿 내용 관리 (수료증 + 이메일)"""
    
    @staticmethod
    def get_content(name: str, season: str, role: str) -> str:
        """수료증 내용 반환"""
        # TODO: 은/는 확인 해주면 좋을 듯!
        role_mapping = {
            "builder": "빌더",
            "runner": "러너"
        }
        role = role_mapping.get(role.lower(), role)
        return f"""{name}은 가짜연구소 {season}기 {role}로서 열정적인 참여와 뛰어난 성과를 보여주었으며, 성장이 멈추는 벽을 부수며 비선형적 성장을 이뤄내고, 우연한 혁명을 이뤄가는 한걸음을 함께 내딛었습니다.

본 수료증은 비영리 연구 공동체에서의 자발적 학습과 협력적 성장을 통해 얻은 소중한 경험과 성취를 증명하며, 기술과 데이터 중심의 의사결정 능력을 기반으로 인간 중심의 인공지능을 이끌어갈 글로벌 테크 리더로 성장할 잠재력을 보여주었습니다. 이를 통해 사회적 가치 창출과 긍정적 임팩트를 만들어가며, 커뮤니티의 지속적인 발전에 기여한 것을 인정합니다."""

    @staticmethod
    def get_email_template(recipient_name: str, course_name: str, season: str, role: str) -> Tuple[str, str]:
        """기본 이메일 템플릿"""
        body = f"""
안녕하세요, {recipient_name}님!

PseudoLab {course_name} {season}기 수료를 축하드립니다! 🎉

📋 활동 정보:
• 스터디명: {course_name}
• 기수: {season}
• 역할: {role}

수료증 파일이 첨부되어 있습니다. 
앞으로도 많은 관심과 참여 부탁드립니다! 🚀

감사합니다.
PseudoLab 드림
        """
        return body