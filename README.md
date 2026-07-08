# 📱 AntiPhishingNLP — NLP 기반 피싱 탐지 서비스

> 🏆 **2023 한국인터넷진흥원(KISA) 사이버보안 AI·빅데이터 챌린지 Track C — 최우수상 (1위)**  
> 한국외국어대학교 데이터청년캠퍼스 딥러닝 기반 자연어처리 과정 팀 프로젝트

스미싱 문자와 보이스피싱 음성을 이중으로 탐지하는 NLP 기반 피싱 감지 시스템입니다.  
텍스트 채널(스미싱)은 KoBERT + KoELECTRA + Att-BiLSTM **3중 앙상블**로, 음성 채널(보이스피싱)은 실시간 STT 변환 후 동일 분류 파이프라인에 투입하는 **멀티채널 구조**로 설계됐습니다.

---

## 🏗️ 시스템 아키텍처

```
[입력 채널]
    ├── 📩 스미싱 문자 (텍스트) ──────────────────────┐
    └── 🎙️ 보이스피싱 음성 → STT(Django) → 텍스트 ──┘
                                                      ↓
                              [Trinity Ensemble Classifier]
                         KoBERT ┬ KoELECTRA ┬ Att-BiLSTM
                                └─── 소프트보팅 ───┘
                                          ↓
                               피싱 / 정상 분류 결과
```

![Trinity Architecture](Phishing%20Detection/trinity.png)

---

## 🔬 모델 설명

### 1. KoBERT
- MLM(Masked Language Modeling) 방식으로 양방향 문맥을 학습한 한국어 BERT
- 스미싱 메시지의 비정상적 언어 구조·은어를 맥락 단위로 이해

### 2. KoELECTRA
- RTD(Replaced Token Detection) 방식으로 문장 내 단어 적합성을 평가하는 한국어 ELECTRA
- 변형된 표현이나 새로운 유형의 스미싱에서도 높은 일반화 성능 발휘

### 3. Att-BiLSTM (Attention + Bidirectional LSTM + MeCab)
- MeCab 형태소 분석기로 한국어 복합어를 세밀하게 분해하여 임베딩
- Attention 메커니즘으로 피싱 의도를 암시하는 핵심 단어에 가중치 집중
- 도메인 특화 최적화로 Transformer 계열 모델의 과소탐지를 보완

### 앙상블 전략
세 모델의 소프트보팅(Soft Voting)으로 최종 판별.  
KoBERT·KoELECTRA의 일반화 능력과 Att-BiLSTM의 도메인 특화 능력을 결합하여, 기존 패턴은 물론 신규 변형 피싱도 포괄적으로 탐지합니다.

---

## 📊 데이터셋

- **스미싱 탐지**: `KorCCViD_v1.3_fullcleansed.csv` (한국 사이버범죄 데이터 정제본)
- **클래스 불균형 대응**: SMOTE(Synthetic Minority Over-sampling Technique) 적용
- **학습/검증 분할**: 불균형 클래스를 고려한 stratified split

---

## 🖥️ 서비스 구성

| 채널 | 기술 | 설명 |
|---|---|---|
| 스미싱 탐지 | Python, KoBERT, KoELECTRA, Att-BiLSTM | 문자 메시지 텍스트 분류 |
| 보이스피싱 탐지 | Django, Web Speech API, STT | 실시간 음성 → 텍스트 → 분류 |

### 보이스피싱 탐지 데모

<img src="README_img/4.gif" width="480"/>

<img src="README_img/1.png" width="400"/>
<img src="README_img/2.png" width="400"/>
<img src="README_img/3.png" width="400"/>

---

## 🚀 실행 방법

### 사전 요구사항
- Python 3.8+
- Django 3.x+

### 텍스트 분류 모듈 (스미싱)
```bash
pip install -r requirements.txt
python main_script.py
```
> ⚠️ KoBERT·KoELECTRA 모델 파일은 용량 문제로 제외되었습니다. 모델링 코드(`Phishing Detection/` 내 `.ipynb`)는 포함되어 있습니다.

### 보이스피싱 탐지 서버 (Django)
```bash
python manage.py runserver
```
브라우저에서 `http://localhost:8000`에 접속하여 마이크로 음성을 입력하면 실시간 탐지 결과를 확인할 수 있습니다.

---

## 📁 주요 파일

| 파일/폴더 | 설명 |
|---|---|
| `Phishing Detection/` | 모델 학습 노트북 (KoBERT, KoELECTRA, Att-BiLSTM, 앙상블) |
| `best_model.h5` | 학습된 Att-BiLSTM 모델 가중치 |
| `KorCCViD_v1.3_fullcleansed.csv` | 정제된 스미싱 학습 데이터셋 |
| `text_classification_module.py` | 스미싱 분류 추론 모듈 |
| `chat/` | Django 보이스피싱 탐지 앱 (views, models, urls) |

---

## 👥 팀 구성 및 기여

**팀명**: 생태계교란조 (한국외국어대학교 데이터청년캠퍼스)  
**팀원**: 홍수빈, **백지헌**, 장영재, 정희수, 이규영

**백지헌 담당 파트**:
- 스미싱 탐지 앙상블 모델 설계 및 구현 (Att-BiLSTM 아키텍처, 앙상블 보팅 전략)
- KorCCViD 데이터셋 정제 및 클래스 불균형 처리 (SMOTE)
- 텍스트 분류 추론 모듈(`text_classification_module.py`) 개발

---

## 📄 License

MIT License
