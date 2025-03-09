# Jupyter Book

Jupyter Book은 .ipynb파일과 .md파일을 활용해 손쉽게 정리된 문서를 만들 수 있는 오픈소스 도구이다. [Project Jupyter](https://jupyter.org/index.html)의 핵심 기여자(contributor)들이 모여 [Executable Book Project](https://executablebooks.org/en/latest/index.html) (EBP)를 시작했고, Jupyter Book은 EBP의 산출물 중 하나이다. .ipynb 파일을 기본 문서 파일로 지원한다는 점에서 데이터 사이언스 업계 종사자 및 학생들에게 적합한 문서 정리 도구라고 생각되며, 오픈소스라는 점에서 가짜연구소의 핵심가치와도 부합해 보인다. 그렇기 때문에 가짜연구소에서는 Jupyter Book을 활용한 자료정리를 진행 중이다. 

## 주요 기능

Jupyter Book의 주요 기능을 요약하자면 아래와 같다. 

- 여러 .ipynb 파일과 .md 파일을 묶어 하나의 웹페이지 구성
- .ipynb파일의 입/출력 셀에 있는 내용을 함께 기록
- Thebe를 활용해 html 페이지 상에서 코드 실행 
- 셀의 Tag기능을 활용해 다방면으로 셀 편집

위에서 언급한 기능 외에도 [Jupyter Book 공식 홈페이지](https://jupyterbook.org/intro.html)에서 다양한 기능들을 언급하고 있다. 

## Jupyter Book 튜토리얼

Jupyter Book 공식 홈페이지에서 사용법을 자세히 정리 해두긴 했지만, 영어로 되어 있어 국내 사용자에겐 진입 장벽이 있을 수 있다. 이번 튜토리얼에서는 한국어로 Jupyter Book 사용법을 정리하고자 한다. 공식 홈페이지에 나와 있는 영문 튜토리얼을 전체 번역하는 것이 아니라, 요점만 간략하게 정리해보고자 한다. 이번 튜토리얼을 따라한다면, Jupyter Book에서 제공하는 기본 template을 본인의 니즈의 맞게 수정하는 방법을 터득할 수 있을 것이다. 

튜토리얼을 시작하기에 앞서 준비해야할 도구들은 다음과 같다. 

- conda와 git 사용이 가능한 CLI (ex. [Anaconda Prompt](https://docs.anaconda.com/anaconda/user-guide/getting-started/))
- Github 계정

튜토리얼 목차는 다음과 같다. 

1. 기본 template 생성
2. template 내용 수정
3. Github Pages를 통한 배포
4. Jupyter Lab을 활용한 셀 Tag 수정
5. Jupytext를 통한 협업