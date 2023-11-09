## NLP 기반 피싱 탐지 서비스
한국외국어대학교 데이터청년캠퍼스 딥러닝기반 자연어처리 과정 프로젝트

생태계교란조: 홍수빈, 백지헌, 장영재, 정희수, 이규영

### 텍스트 분류
1. main_scirpt:  test_classification_module모듈을 불러와 실행하는 파일.
2. test_classification_module.py: 실제 기능 구현된 모듈. 모델과 데이터셋 경로 설정 필요.
3. AttBiLSTM_2K: 모델 파일. 
4. intergrated_unbalan5.csv: 데이터셋 파일.

### 음성 분류 
Django Speech to text, Voise Phishing detecter
입력된 음성 파일을 실시간으로 STT 처리하여 변환한 결과를 KOBERT, BILSTM 모델로 보이스피싱인지 유무 검출

#### Commands to Setup the environment and run the server

> git clone https://github.com/urinaner/voice_phishing.git

> cd Django-Speech-to-text-Chat

> virtualenv venv

> source venv/bin/activate

> pip install -r requirements.txt

> python manage.py runserver

<img src="README_img/4.gif" width="400" height="300"/>

<img src="README_img/1.png" width="400" height="300"/>
<br/>
<img src="README_img/2.png" width="400" height="300"/>
<br/>
<img src="README_img/3.png" width="400" height="300"/>

