# 📱 AntiPhishingNLP — NLPベースのフィッシング検出サービス

**🌐 Available Versions:** [🇺🇸 English](/README.md) | [🇰🇷 한국어 (Korean)](/README_KR.md)

> 🏆 **2023年 韓国インターネット振興院（KISA）サイバーセキュリティ AI・ビッグデータチャレンジ Track C — 最優秀賞（1位）**  
> 韓国外国語大学 データユースキャンパス ディープラーニングベース自然言語処理課程 チームプロジェクト

> 📌 **前作プロジェクト：** [SepticFilterNLP](https://github.com/fairyofdata/SepticFilterNLP)（三星SDS マルチキャンパス最優秀賞、2022年）で構築した字母トークン化戦略・アンサンブル設計・コミュニティクローリング経験が、本プロジェクトの技術的基盤となっています。

スミッシング（SMS フィッシング）とボイスフィッシング（音声詐欺）を同時に検出する、デュアルチャネル NLP フィッシング検知システムです。  
テキストチャネル（スミッシング）は KoBERT + KoELECTRA + Att-BiLSTM の **3 重アンサンブル**で判別します（`Phishing Detection/` のノートブック）。音声チャネル（ボイスフィッシング）は別の Django デモで、Google Web Speech API で文字起こしした後、アンサンブルではなく専用の単一 LSTM モデル（`best_model.h5`）で分類します。

---

## 🏗️ システムアーキテクチャ

```
[テキストチャネル — ノートブック]
    📩 スミッシング SMS（テキスト）
        → [Trinity Ensemble: KoBERT ┬ KoELECTRA ┬ Att-BiLSTM → ソフト投票]
        → フィッシング / 正常

[音声チャネル — Django デモ]
    🎙️ 音声 → Google Web Speech API（STT）→ テキスト
        → [単一 LSTM 分類器: best_model.h5]
        → ボイスフィッシング確率
```

![Trinity Architecture](Phishing%20Detection/trinity.png)

---

## 🔬 モデル詳細

### 1. KoBERT
- MLM（Masked Language Modeling）方式で双方向文脈を学習した韓国語 BERT
- スミッシングメッセージに含まれる異常な言語構造・隠語を文脈単位で把握

### 2. KoELECTRA
- RTD（Replaced Token Detection）方式で文中の単語適合性を評価する韓国語 ELECTRA
- 変形表現や新手口のスミッシングに対しても高い汎化性能を発揮

### 3. Att-BiLSTM（Attention + 双方向 LSTM + MeCab）
- MeCab 形態素解析器で韓国語複合語を細かく分解してエンベディング
- Attention 機構によりフィッシング意図を示すキーワードに重みを集中
- ドメイン特化の最適化で Transformer 系モデルの見落としを補完

### アンサンブル戦略
3 モデルの**ソフト投票（Soft Voting）**で最終判定を実施。  
KoBERT・KoELECTRA の汎化能力と Att-BiLSTM のドメイン特化精度を組み合わせ、既知のパターンだけでなく新手口のフィッシングも網羅的に検出します。

---

## 📊 データセット

| 項目 | 詳細 |
|---|---|
| **データセット** | `KorCCViD_v1.3_fullcleansed.csv`（韓国サイバー犯罪データ 精製版） |
| **クラス不均衡対策** | SMOTE（Synthetic Minority Over-sampling Technique）適用 |
| **学習 / 検証分割** | クラス分布を考慮した Stratified Split |

---

## 🖥️ サービス構成

| チャネル | 技術 | 説明 |
|---|---|---|
| スミッシング検出 | Python, KoBERT, KoELECTRA, Att-BiLSTM | SMS テキスト分類パイプライン |
| ボイスフィッシング検出 | Django, Web Speech API, STT | リアルタイム音声 → テキスト → 分類 |

### ボイスフィッシング検出デモ

<img src="README_img/4.gif" width="480"/>

<img src="README_img/1.png" width="400"/>
<img src="README_img/2.png" width="400"/>
<img src="README_img/3.png" width="400"/>

---

## 🚀 実行方法

### 前提条件
- Python 3.8+
- Django 3.x+

### テキスト分類モジュール（スミッシング）
```bash
pip install -r requirements.txt
python main_script.py
```
> ⚠️ KoBERT・KoELECTRA のモデルファイルはサイズの都合でリポジトリから除外されています。モデリングコード（`Phishing Detection/` 内の `.ipynb`）は含まれています。

### ボイスフィッシング検出サーバー（Django）
```bash
python manage.py runserver
```
ブラウザで `http://localhost:8000` にアクセスし、マイクに向かって話しかけるとリアルタイムで判定結果が表示されます。

---

## 📁 主要ファイル

| ファイル / フォルダ | 説明 |
|---|---|
| `Phishing Detection/` | モデル学習ノートブック（KoBERT, KoELECTRA, Att-BiLSTM, アンサンブル） |
| `best_model.h5` | 音声デモ用の学習済み LSTM モデルの重み（Embedding → LSTM → Dense） |
| `KorCCViD_v1.3_fullcleansed.csv` | 精製済みスミッシング学習データセット |
| `text_classification_module.py` | スミッシング分類推論モジュール |
| `chat/` | Django ボイスフィッシング検出アプリ（views, models, urls） |

---

## 👥 チーム構成と貢献

**チーム名**：생태계교란조（エコシステム・ディスラプターズ）、韓国外国語大学 データユースキャンパス  
**メンバー**：홍수빈、**백지헌**、장영재、정희수、이규영

**백지헌 の担当パート**：
- Att-BiLSTM の構成の提案（単純な LSTM の代わりに、双方向 LSTM に Attention 層を加える）
- クラス不均衡に対する SMOTE の適用の提案

---

## 📄 License

MIT License
