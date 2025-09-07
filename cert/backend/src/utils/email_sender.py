import asyncio
import os
import aiohttp
import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from typing import Optional

class EmailSender:
    """이메일 발송 유틸리티"""
    
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = "manage.timekeeper@gmail.com"
        self.smtp_password = "oroj jyiv sumi qbly"
        
        # 디버깅 정보 출력
        print(f"🔧 SMTP 설정 로드:")
        print(f"  HOST: {self.smtp_host}")
        print(f"  PORT: {self.smtp_port}")
        print(f"  USERNAME: {self.smtp_username}")
        print(f"  PASSWORD: {'********  ' if self.smtp_password else 'None'}")
    
    async def send_certificate_email(
        self, 
        recipient_email: str, 
        recipient_name: str,
        course_name: str,
        season: str, 
        role: str,
        certificate_path: Optional[str] = None,
        certificate_bytes: Optional[bytes] = None
    ) -> bool:
        """수료증 이메일 발송"""
        try:
            print(f"📧 이메일 발송 시도: {recipient_email}")
            print(f"  발신자: {self.smtp_username}")
            print(f"  SMTP 서버: {self.smtp_host}:{self.smtp_port}")
            
            if not all([self.smtp_username, self.smtp_password]):
                print("❌ SMTP 설정이 완료되지 않았습니다.")
                print(f"  USERNAME: {self.smtp_username}")
                print(f"  PASSWORD: {'설정됨' if self.smtp_password else '설정되지 않음'}")
                return False
            
            # 이메일 메시지 생성
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = recipient_email
            msg['Subject'] = f"[PseudoLab] {course_name} 수료증 발급 완료 🎉"
            
            # 이메일 본문
            body = f"""
안녕하세요, {recipient_name}님!

PseudoLab {course_name} {season} 수료를 축하드립니다! 🎉

🎯 활동 정보
• 스터디명: {course_name}
• 기수: {season}
• 역할: {role}

수료증이 첨부되어 있습니다. 
PseudoLab에서의 소중한 시간이 되었기를 바랍니다.

앞으로도 많은 관심과 참여 부탁드립니다! 🚀

감사합니다.
PseudoLab 팀
            """
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # 수료증 첨부 (바이트 데이터 우선)
            if certificate_bytes:
                pdf_attachment = MIMEApplication(certificate_bytes, _subtype='pdf')
                pdf_attachment.add_header('Content-Disposition', 'attachment', filename=f'certificate_{recipient_name}.pdf')
                msg.attach(pdf_attachment)
                print(f"📎 PDF 첨부 완료 (메모리): {len(certificate_bytes)} bytes")
            elif certificate_path and os.path.exists(certificate_path):
                with open(certificate_path, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-Disposition', 'attachment', filename='certificate.jpg')
                    msg.attach(img)
                print(f"📎 이미지 첨부 완료: {certificate_path}")
            
            # 이메일 발송
            async with aiosmtplib.SMTP(
                hostname=self.smtp_host,
                port=self.smtp_port,
                use_tls=False  # 포트 587은 STARTTLS 사용
            ) as smtp:
                # STARTTLS는 aiosmtplib가 자동으로 처리
                await smtp.login(self.smtp_username, self.smtp_password)
                await smtp.send_message(msg)
            
            print(f"✅ 수료증 이메일 발송 완료: {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ 이메일 발송 중 오류: {e}")
            return False
    
    async def send_error_notification(
        self,
        recipient_email: str,
        error_message: str
    ) -> bool:
        """오류 알림 이메일 발송"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = recipient_email
            msg['Subject'] = "[PseudoLab] 수료증 발급 오류 안내"
            
            body = f"""
안녕하세요!

수료증 발급 처리 중 오류가 발생했습니다.

❌ 오류 내용: {error_message}

디스코드를 통해 김수현(kyopbi)에게 문의해주세요.

감사합니다.
PseudoLab 팀
            """
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            async with aiosmtplib.SMTP(
                hostname=self.smtp_host,
                port=self.smtp_port,
                use_tls=False  # 포트 587은 STARTTLS 사용
            ) as smtp:
                # STARTTLS는 aiosmtplib가 자동으로 처리
                await smtp.login(self.smtp_username, self.smtp_password)
                await smtp.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"❌ 오류 알림 이메일 발송 중 오류: {e}")
            return False


if __name__ == "__main__":
    async def main():
        print("=== 이메일 발송 테스트 ===")
        
        # 환경 변수 확인
        smtp_username = "bailando.ys@gmail.com"
        smtp_password = ""
        
        print(f"SMTP_USERNAME: {'✅ 설정됨' if smtp_username else '❌ 설정되지 않음'}")
        print(f"SMTP_PASSWORD: {'✅ 설정됨' if smtp_password else '❌ 설정되지 않음'}")
        
        if not all([smtp_username, smtp_password]):
            print("\n❌ SMTP 설정이 완료되지 않았습니다!")
            print("1. .env 파일에 SMTP 설정을 추가하세요")
            print("2. Gmail 사용 시 앱 비밀번호를 생성하세요")
            print("3. 2단계 인증을 활성화하세요")
            return
        
        print("\n📧 테스트 이메일 발송 중...")
        
        email_sender = EmailSender()
        success = await email_sender.send_certificate_email(
            recipient_email="bailando.ys@gmail.com",  # 실제 테스트할 이메일로 변경
            recipient_name="테스트 사용자",
            course_name="테스트 스터디",
            season="10기",
            role="BUILDER"
        )
        
        if success:
            print("✅ 테스트 이메일 발송 성공!")
        else:
            print("❌ 테스트 이메일 발송 실패!")
    
    asyncio.run(main())
