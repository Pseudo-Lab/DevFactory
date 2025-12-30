import logging
import os
import requests
import tarfile
import tempfile
import subprocess
from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .template_content import TemplateContent


logger = logging.getLogger(__name__)

class PDFGenerator:
    """PDF 인증서 """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # 색상
        self.text_color = [19/255, 34/255, 43/255]  # #13222B
        
        # 기본 크기
        self.default_width = 1528
        self.default_height = 1080
        
        # 폰트 설정
        self.font_urls = {
            'IBMPlexSansKR-Regular': "https://github.com/google/fonts/raw/main/ofl/ibmplexsanskr/IBMPlexSansKR-Regular.ttf",
            'IBMPlexSansKR-Bold': "https://github.com/google/fonts/raw/main/ofl/ibmplexsanskr/IBMPlexSansKR-Bold.ttf",
        }
        
        # 텍스트 위치 설정
        self.positions = {
            "season": {"x": 299, "y": 1080 - 326 - 30, "font_size": 32, "char_space": -1.2},
            "content": {"x": 299, "y": 1080 - 485 - 65, "font_size": 26, "char_space": -0.5},
            "name": {"x": 299, "y": 1080 - 902 - 65, "font_size": 72, "char_space": -1.2},
        }
        
        # 텍스트 설정
        self.line_height_ratio = 1.5
        self.char_width_ratio = 0.5  # 0.6에서 0.5로 줄임
        self.chars_per_line = 75
        self.text_wrap_threshold = 30
        
        # 파일명 설정
        self.certificate_prefix = "certificate_"
        self.certificate_suffix = ".pdf"
        self.certificate_number_format = "{:03d}"
        
        # 경로 설정
        self.font_dir_name = "fonts"
        self.template_dir_name = "templates"
        self.template_archive_password_env = "CERT_TEMPLATE_ARCHIVE_PASSWORD"
        self.certificate_dir_name = "certificates"
        
        # 기본 템플릿
        self.ds_template = "ds.png"
        self.builder_template = "builder.png"
        self.runner_template = "runner.png"
        self.template_archive_name = "templates.tar.gz"
        self.template_archive_enc_name = f"{self.template_archive_name}.enc"
        self.required_templates = [
            self.ds_template,
            self.builder_template,
            self.runner_template,
        ]
        
        # 폰트 로드 상태
        self._fonts_loaded = False
        self._initialized = True


    def get_asset_path(self, asset_type, filename=None):
        """자산 경로 반환"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        if asset_type == self.font_dir_name:
            return os.path.join(current_dir, f"../assets/{self.font_dir_name}")
        elif asset_type == self.template_dir_name:
            return os.path.join(current_dir, f"../assets/{self.template_dir_name}")
        elif asset_type == self.certificate_dir_name:
            return os.path.join(current_dir, f"../../{self.certificate_dir_name}")
        elif asset_type == "template_file":
            template_dir = self.get_asset_path(self.template_dir_name)
            return os.path.join(template_dir, filename or self.ds_template)
        elif asset_type == "ds_template":
            template_dir = self.get_asset_path(self.template_dir_name)
            return os.path.join(template_dir, self.ds_template)
        elif asset_type == "runner_template":
            template_dir = self.get_asset_path(self.template_dir_name)
            return os.path.join(template_dir, self.runner_template)
        elif asset_type == "builder_template":
            template_dir = self.get_asset_path(self.template_dir_name)
            return os.path.join(template_dir, self.builder_template)
        else:
            raise ValueError(f"알 수 없는 자산 타입: {asset_type}")


    def _download_fonts(self):
        """폰트 다운로드 및 등록"""
        if self._fonts_loaded:
            return
            
        font_dir = self.get_asset_path(self.font_dir_name)
        os.makedirs(font_dir, exist_ok=True)
        
        # 한글 폰트 다운로드 및 등록
        for name, url in self.font_urls.items():
            font_path = os.path.join(font_dir, f"{name}.ttf")
            
            if not os.path.exists(font_path):
                try:
                    response = requests.get(url, timeout=30)
                    with open(font_path, 'wb') as f:
                        f.write(response.content)
                    logger.info("폰트 다운로드 완료", extra={"font_name": name})
                except Exception:
                    logger.exception("폰트 다운로드 실패", extra={"font_name": name})
            
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont(name, font_path))
                logger.info("폰트 등록 완료", extra={"font_name": name})
        
        # 영어 폰트 등록
        english_font_path = os.path.join(font_dir, "HeptaSlab-SemiBold.ttf")
        
        if os.path.exists(english_font_path):
            pdfmetrics.registerFont(TTFont('HeptaSlab-SemiBold', english_font_path))
            logger.info("HeptaSlab-SemiBold 폰트 등록 완료")
        else:
            logger.warning("HeptaSlab-SemiBold.ttf 파일을 찾을 수 없습니다.")
        
        self._fonts_loaded = True

    def _get_image_size(self, template_path):
        """이미지 크기 확인"""
        try:
            with open(template_path, 'rb') as f:
                if f.read(8) == b'\x89PNG\r\n\x1a\n':
                    f.seek(16)
                    width = int.from_bytes(f.read(4), byteorder='big')
                    height = int.from_bytes(f.read(4), byteorder='big')
                else:
                    width, height = self.default_width, self.default_height
        except:
            width, height = self.default_width, self.default_height
        
        return width, height

    def _get_next_certificate_path(self):
        """다음 인증서 파일 경로 생성"""
        output_dir = self.get_asset_path(self.certificate_dir_name)
        os.makedirs(output_dir, exist_ok=True)
        
        counter = 1
        while True:
            filename = self.certificate_prefix + self.certificate_number_format.format(counter) + self.certificate_suffix
            output_path = os.path.join(output_dir, filename)
            if not os.path.exists(output_path):
                return output_path
            counter += 1

    def _draw_text(self, canvas_obj, text, x, y, font_name, font_size, char_space=0, auto_font=False, korean_font=None, english_font=None):
        """텍스트 그리기 (통합 함수)"""
        # 색상 설정
        canvas_obj.setFillColorRGB(*self.text_color)
        
        if auto_font and korean_font and english_font:
            # 프로젝트 이름용: 한/영 자동 폰트 선택
            self._draw_text_with_spacing(canvas_obj, text, x, y, font_size, korean_font, english_font, char_space)
        else:
            # 일반 텍스트용: 지정된 폰트 사용
            self._draw_text_with_spacing(canvas_obj, text, x, y, font_size, font_name, font_name, char_space)

    def _draw_multiline_text(self, canvas_obj, text, x, y, font_name, font_size, char_space=0):
        """여러 줄 텍스트 그리기"""
        lines = text.split('\n')
        line_height = font_size * self.line_height_ratio
        total_height = len(lines) * line_height
        start_y = y + total_height / 2
        
        for i, line in enumerate(lines):
            line_y = start_y - i * line_height
            
            if len(line) > self.text_wrap_threshold:
                for j in range(0, len(line), self.chars_per_line):
                    chunk = line[j:j + self.chars_per_line].strip()
                    self._draw_text(canvas_obj, chunk, x, line_y, font_name, font_size, char_space)
                    line_y -= line_height
            else:
                self._draw_text(canvas_obj, line, x, line_y, font_name, font_size, char_space)

    def _draw_text_with_spacing(self, canvas, text, x, y, font_size, korean_font, english_font, char_space=0):
        """텍스트 그리기 (자간 조정 포함)"""
        current_x = x
        
        for i, char in enumerate(text):
            # 폰트 선택
            if "가" <= char <= "힣":  # 한글
                canvas.setFont(korean_font, font_size)
            else:  # 영어/숫자/기호
                canvas.setFont(english_font, font_size)
            
            # 문자 그리기
            char_width = canvas.stringWidth(char)
            canvas.drawString(current_x, y, char)
            
            # 자간 조정
            current_x += char_width + (char_space if i < len(text) - 1 else 0)
        
        return current_x - x

    def _measure_text_width(self, text, font_size, korean_font, english_font, char_space=0):
        """텍스트의 전체 너비 측정"""
        total_width = 0
        for i, char in enumerate(text):
            if "가" <= char <= "힣":
                # 한글 폰트로 너비 측정 (임시 캔버스 사용)
                temp_canvas = canvas.Canvas(BytesIO())
                temp_canvas.setFont(korean_font, font_size)
                char_width = temp_canvas.stringWidth(char)
            else:
                # 영어 폰트로 너비 측정
                temp_canvas = canvas.Canvas(BytesIO())
                temp_canvas.setFont(english_font, font_size)
                char_width = temp_canvas.stringWidth(char)
            
            total_width += char_width + (char_space if i < len(text) - 1 else 0)
        
        return total_width

    def _wrap_text_by_width(self, text, font_size, korean_font, english_font, char_space=0, max_width=1000):
        """텍스트를 너비에 맞게 자동 개행"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            test_width = self._measure_text_width(test_line, font_size, korean_font, english_font, char_space)
            
            if test_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    # 단어 자체가 너무 긴 경우 강제로 자르기
                    lines.append(word)
                    current_line = ""
        
        if current_line:
            lines.append(current_line)

        return lines

    def create_certificate(self, name:str, season: int, course_name:str, role:str, period:str="", save_file:bool=False, output_path:str=None):
        """인증서 생성 (기본적으로 bytes 반환, 옵션으로 파일 저장)"""
        self._download_fonts()
        self._prepare_templates()
        
        # 경로 설정
        if role == "BUILDER":
            template_path = self.get_asset_path("builder_template")
        elif role == "RUNNER":
            template_path = self.get_asset_path("runner_template")
        else:
            template_path = self.get_asset_path("ds_template")
        
        # 이미지 크기 확인
        width, height = self._get_image_size(template_path)
        
        # PDF 생성 (항상 메모리에서 시작)
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=(width, height))
        
        # 배경 이미지
        if os.path.exists(template_path):
            c.drawImage(template_path, 0, 0, width, height)
            logger.info("템플릿 이미지 추가", extra={"template_path": template_path})
        else:
            raise ValueError(
                f"템플릿 이미지를 찾을 수 없습니다: {template_path}. "
                f"템플릿 디렉터리에 필수 PNG가 있는지 확인하세요."
            )
        
        # Season 정보 설정
        season_english = f"Season {season} ({period['start']} ~ {period['end']}) / "
        season_korean = course_name
        
        # 폰트 설정
        english_font = 'HeptaSlab-SemiBold' if 'HeptaSlab-SemiBold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
        korean_font = 'IBMPlexSansKR-Regular' if 'IBMPlexSansKR-Regular' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
        korean_bold_font = 'IBMPlexSansKR-Bold' if 'IBMPlexSansKR-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
        
        # 1. Season 정보
        season_config = self.positions['season']
        season_x = season_config['x']
        season_y = season_config['y']
        season_font_size = season_config['font_size']
        season_char_space = season_config.get('char_space', 0)
        
        # 프로젝트 이름: 기수는 고정, 코스명만 개행 처리
        project_x = season_x
        project_y = season_y
        
        # 첫 번째 줄: 기수 정보 (예: "10기 /")
        first_line = season_english + " "
        self._draw_text(c, first_line, project_x, project_y, english_font, season_font_size, season_char_space)
        
        # 코스명 길이 측정
        course_width = self._measure_text_width(season_korean, season_font_size, korean_bold_font, english_font, season_char_space)
        first_line_width = self._measure_text_width(first_line, season_font_size, english_font, english_font, season_char_space)
        remaining_width = 1000 - first_line_width  # 첫 줄 이후 남은 너비
        
        if course_width <= remaining_width:
            # 코스명이 남은 공간에 들어가면 같은 줄에 그리기
            course_x = project_x + first_line_width
            self._draw_text(c, season_korean, course_x, project_y, None, season_font_size, season_char_space,
                          auto_font=True, korean_font=korean_bold_font, english_font=english_font)
            total_extra_height = 0
        else:
            # 코스명이 길면 다음 줄부터 개행
            lines = self._wrap_text_by_width(season_korean, season_font_size, korean_bold_font, english_font, season_char_space, 1200)
            normal_line_height = season_font_size * 1.2
            tight_line_height = season_font_size * 1.0
            
            for i, line in enumerate(lines):
                if i == 0:
                    # 첫 번째 개행: 일반 행간
                    line_y = project_y - normal_line_height
                else:
                    # 두 번째 개행부터: 축소된 행간
                    line_y = project_y - normal_line_height - (i * tight_line_height)
                
                self._draw_text(c, line, project_x, line_y, None, season_font_size, season_char_space,
                              auto_font=True, korean_font=korean_bold_font, english_font=english_font)
            
            # 총 높이 계산: 첫 개행(일반) + 나머지 개행(축소)
            total_extra_height = normal_line_height + (len(lines) - 1) * tight_line_height

        
        
        # 2. 내용 (프로젝트 이름 길이에 따라 위치 조정)
        content = TemplateContent.get_content(name, season, role)
        
        content_config = self.positions['content']
        content_x = content_config['x']
        content_y = content_config['y'] - total_extra_height  # 프로젝트 이름이 길면 아래로 이동
        content_font_size = content_config['font_size']
        content_char_space = content_config.get('char_space', 0)
        
        self._draw_multiline_text(c, content, content_x, content_y, korean_font, content_font_size, content_char_space)
        
        # 3. 이름
        name_config = self.positions['name']
        name_x = name_config['x']
        name_y = name_config['y']
        name_font_size = name_config['font_size']
        name_char_space = name_config.get('char_space', 0)
        
        self._draw_text(c, name, name_x, name_y, korean_font, name_font_size, name_char_space)
        
        # PDF 저장
        c.save()
        
        # 메모리에서 PDF 바이트 가져오기
        buffer.seek(0)
        pdf_bytes = buffer.getvalue()
        
        # 파일 저장 옵션이 활성화된 경우
        if save_file:
            if output_path is None:
                output_path = self._get_next_certificate_path()
            
            # 바이트를 파일로 저장
            with open(output_path, 'wb') as f:
                f.write(pdf_bytes)
            logger.info("인증서 파일 저장 완료", extra={"output_path": output_path})
        
        buffer.close()
        logger.info(
            "인증서 생성 완료",
            extra={
                "recipient_name": name,
                "season": season,
                "role": role,
                "saved_to_file": save_file,
            },
        )
        return pdf_bytes

    def _templates_exist(self, template_dir: str) -> bool:
        """필수 템플릿이 모두 존재하는지 확인"""
        return all(os.path.exists(os.path.join(template_dir, name)) for name in self.required_templates)

    def _prepare_templates(self):
        """템플릿 디렉터리를 준비하고 없으면 복호화/압축 해제"""
        template_dir = self.get_asset_path(self.template_dir_name)
        os.makedirs(template_dir, exist_ok=True)

        if self._templates_exist(template_dir):
            return

        # 아카이브 경로 설정
        base_archive_path = os.path.join(template_dir, self.template_archive_name)

        if base_archive_path.endswith(".enc"):
            encrypted_archive_path = base_archive_path
            archive_path = base_archive_path[:-4]
        else:
            archive_path = base_archive_path
            encrypted_archive_path = f"{base_archive_path}.enc"

        # 복호화 + 압축 해제 시도
        temp_decrypted_path = None
        try:
            if os.path.exists(archive_path):
                self._extract_archive(archive_path, template_dir)
            elif os.path.exists(encrypted_archive_path):
                password = os.getenv(self.template_archive_password_env)
                if not password:
                    raise ValueError(
                        f"암호화된 템플릿 아카이브를 복호화하려면 {self.template_archive_password_env} "
                        f"환경변수가 필요합니다. 경로: {encrypted_archive_path}"
                    )
                temp_decrypted_path = self._decrypt_archive(encrypted_archive_path, password)
                self._extract_archive(temp_decrypted_path, template_dir)
            else:
                raise ValueError(
                    "템플릿 파일을 찾을 수 없습니다. "
                    f"{template_dir} 아래에 필수 PNG 또는 {self.template_archive_name}[.enc]을 배치하세요."
                )
        finally:
            if temp_decrypted_path and os.path.exists(temp_decrypted_path):
                os.remove(temp_decrypted_path)

        if not self._templates_exist(template_dir):
            raise ValueError(
                f"템플릿 압축 해제 후에도 필수 템플릿이 없습니다. 경로: {template_dir}"
            )

    def _decrypt_archive(self, encrypted_path: str, password: str) -> str:
        """openssl로 .enc 아카이브 복호화"""
        fd, temp_path = tempfile.mkstemp(suffix=".tar.gz")
        os.close(fd)

        result = subprocess.run(
            [
                "openssl",
                "enc",
                "-d",
                "-aes-256-cbc",
                "-pbkdf2",
                "-in",
                encrypted_path,
                "-out",
                temp_path,
                "-pass",
                f"pass:{password}",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise ValueError(
                f"템플릿 아카이브 복호화 실패: {result.stderr.strip() or result.stdout.strip()}"
            )

        return temp_path

    def _extract_archive(self, archive_path: str, target_dir: str):
        """tar.gz 아카이브 압축 해제"""
        if not tarfile.is_tarfile(archive_path):
            raise ValueError(f"유효하지 않은 아카이브 파일입니다: {archive_path}")

        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=target_dir)




if __name__ == "__main__":
    # 테스트

    long_name_project = ["From Fixed to Flexible: Your Guide to Adaptive & Master Protocol",
                         "< Bridging >",
                         "DevFactory",
                         "Marketing Science : Marketing Data Analytics & Bayesian Statistics",
                         "Developer can link the world : 세상을 잇다"
    ]

    generator = PDFGenerator()
    generator.create_certificate(
        name="김예신",
        season=11,
        course_name=long_name_project[2],
        role="RUNNER",
        period={"start": "2025-01-01", "end": "2025-01-01"},
        save_file=True,
    )
