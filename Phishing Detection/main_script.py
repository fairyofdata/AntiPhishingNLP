# text_classification_module.py를 불러온다. 
from text_classification_module import TextClassifier

def main():
    model_save_path = "/content/drive/MyDrive/AttBiLSTM_2K"
    classifier = TextClassifier(model_save_path)

    example_text = input("대화를 입력하세요. (최소 50자/20어절/2문장 이상)")
    result = classifier.classify_text(example_text)
    
    for label, prob in result.items():
        print(f"{int(prob * 100)}% 확률로 {label} 라벨로 분류됩니다.")


if __name__ == "__main__":
    main()