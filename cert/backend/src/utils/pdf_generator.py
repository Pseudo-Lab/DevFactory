import os
import requests
import zipfile
import subprocess
from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .template_content import TemplateContent

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
            "content": {"x": 299, "y": 1080 - 385 - 65, "font_size": 20, "max_width": 1131, "char_space": -0.5},
            "name": {"x": 299, "y": 1080 - 902 - 65, "font_size": 72, "char_space": -1.2},
        }
        
        # 텍스트 설정
        self.line_height_ratio = 1.5
        self.char_width_ratio = 0.5  # 0.6에서 0.5로 줄임
        self.chars_per_line = 80
        self.text_wrap_threshold = 45
        
        # 파일명 설정
        self.certificate_prefix = "certificate_"
        self.certificate_suffix = ".pdf"
        self.certificate_number_format = "{:03d}"
        
        # 경로 설정
        self.font_dir_name = "fonts"
        self.template_dir_name = "templates"
        self.certificate_dir_name = "certificates"
        
        # 기본 템플릿
        self.default_template = "default.png"
        self.builder_template = "default0.png"
        self.runner_template = "default1.png"
        
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
            return os.path.join(template_dir, filename or self.default_template)
        elif asset_type == "runner_template":
            template_dir = self.get_asset_path(self.template_dir_name)
            return os.path.join(template_dir, self.runner_template)
        elif asset_type == "builder_template":
            template_dir = self.get_asset_path(self.template_dir_name)
            return os.path.join(template_dir, self.builder_template)
        else:
            raise ValueError(f"알 수 없는 자산 타입: {asset_type}")

    def _download_english_font(self, font_dir):
        """영어 폰트 자동 다운로드 및 압축 해제"""
        zip_path = os.path.join(font_dir, "hepta-slab.zip")
        
        try:
            # TODO: 영어 폰트 임의로 다운로드 해줘야 함. (아래 로직 작동되지 않음)
            print("영어 폰트 다운로드 중...")
            subprocess.run([
                "wget", 
                "https://fontmeme.com/fonts/download/305890/hepta-slab.zip",
                "-O", zip_path
            ], check=True)
            print("영어 폰트 다운로드 완료")
            
            # 압축 해제
            print("압축 해제 중...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(font_dir)
            print("압축 해제 완료")
            
            # HeptaSlab-SemiBold.ttf 파일 찾기
            for root, dirs, files in os.walk(font_dir):
                for file in files:
                    if "HeptaSlab-SemiBold.ttf" in file:
                        source_path = os.path.join(root, file)
                        target_path = os.path.join(font_dir, "HeptaSlab-Bold.ttf")
                        if source_path != target_path:
                            os.rename(source_path, target_path)
                        print("HeptaSlab-Bold.ttf 파일 준비 완료")
                        break
            
            # 임시 파일 정리
            if os.path.exists(zip_path):
                os.remove(zip_path)
            
        except subprocess.CalledProcessError:
            print("wget 명령어 실행 실패. wget이 설치되어 있는지 확인해주세요.")
        except zipfile.BadZipFile:
            print("압축 파일이 손상되었습니다.")
        except Exception as e:
            print(f"영어 폰트 다운로드 중 오류 발생: {e}")

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
                    print(f"{name} 폰트 다운로드 완료")
                except:
                    print(f"{name} 폰트 다운로드 실패")
            
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont(name, font_path))
                print(f"{name} 폰트 등록 완료")
        
        # 영어 폰트 자동 다운로드 및 등록
        english_font_path = os.path.join(font_dir, "HeptaSlab-SemiBold.ttf")
        if not os.path.exists(english_font_path):
            self._download_english_font(font_dir)
        
        if os.path.exists(english_font_path):
            pdfmetrics.registerFont(TTFont('HeptaSlab-SemiBold', english_font_path))
            print("HeptaSlab-SemiBold 폰트 등록 완료")
        else:
            print("HeptaSlab-SemiBold.ttf 파일을 찾을 수 없습니다.")
        
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

    def _draw_text(self, canvas_obj, text, x, y, font_name, font_size, char_space=0):
        """텍스트 그리기"""
        textobject = canvas_obj.beginText()
        textobject.setTextOrigin(x, y)
        textobject.setFont(font_name, font_size)
        textobject.setCharSpace(char_space)
        textobject.setFillColorRGB(*self.text_color)
        textobject.textLine(text)
        canvas_obj.drawText(textobject)

    def _draw_multiline_text(self, canvas_obj, text, x, y, max_width, font_name, font_size, char_space=0):
        """여러 줄 텍스트 그리기"""
        lines = text.split('\n')
        line_height = font_size * self.line_height_ratio
        total_height = len(lines) * line_height
        start_y = y + total_height / 2
        
        for i, line in enumerate(lines):
            line_y = start_y - i * line_height
            
            if len(line) > self.text_wrap_threshold:
                for j in range(0, len(line), self.chars_per_line):
                    chunk = line[j:j + self.chars_per_line]
                    self._draw_text(canvas_obj, chunk, x, line_y, font_name, font_size, char_space)
                    line_y -= line_height
            else:
                self._draw_text(canvas_obj, line, x, line_y, font_name, font_size, char_space)


    def create_certificate(self, name:str, season: int, course_name:str, role:str, period:str="", save_file:bool=False, output_path:str=None):
        """인증서 생성 (기본적으로 bytes 반환, 옵션으로 파일 저장)"""
        self._download_fonts()
        
        # 경로 설정
        if role == "BUILDER":
            template_path = self.get_asset_path("builder_template")
        elif role == "RUNNER":
            template_path = self.get_asset_path("runner_template")
        else:
            template_path = self.get_asset_path("default_template")
        
        # 이미지 크기 확인
        width, height = self._get_image_size(template_path)
        
        # PDF 생성 (항상 메모리에서 시작)
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=(width, height))
        
        # 배경 이미지
        if os.path.exists(template_path):
            c.drawImage(template_path, 0, 0, width, height)
            print(f"템플릿 이미지 추가: {template_path}")
        else:
            raise ValueError("템플릿 이미지를 찾을 수 없습니다.")
        
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
        
        self._draw_text(c, season_english, season_x, season_y, english_font, season_font_size, season_char_space)
        self._draw_text(c, season_korean, season_x + (len(season_english) - 0.5) * season_font_size * self.char_width_ratio, season_y, korean_bold_font, season_font_size, season_char_space)
        
        
        # 2. 내용
        content = TemplateContent.get_content(name, season, role)
        
        content_config = self.positions['content']
        content_x = content_config['x']
        content_y = content_config['y']
        content_font_size = content_config['font_size']
        content_max_width = content_config['max_width']
        content_char_space = content_config.get('char_space', 0)
        
        self._draw_multiline_text(c, content, content_x, content_y, content_max_width, korean_font, content_font_size, content_char_space)
        
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
            print(f"인증서 파일 저장 완료: {output_path}")
        
        buffer.close()
        print(f"인증서 생성 완료 (메모리)")
        return pdf_bytes




if __name__ == "__main__":
    # 테스트
    generator = PDFGenerator()
    generator.create_certificate(
        name="김예신",
        season=11,
        course_name="DevFactory 기술과사고력이 쑥쑥 넘쳐나는 곳",
        role="BUILDER",
        period={"start": "2025-01-01", "end": "2025-01-01"},
        save_file=True
    )
