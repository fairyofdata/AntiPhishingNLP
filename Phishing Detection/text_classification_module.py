import torch
import torch.nn as nn
from transformers import ElectraTokenizer
from torch.utils.data import DataLoader, TensorDataset

class Attention(nn.Module):
    def __init__(self, hidden_size):
        super(Attention, self).__init__()
        self.hidden_size = hidden_size
        self.W = nn.Linear(hidden_size, hidden_size)
        self.v = nn.Linear(hidden_size, 1, bias=False)

    def forward(self, encoder_outputs):
        energy = torch.tanh(self.W(encoder_outputs))
        attention_scores = self.v(energy).squeeze(2)
        attention_weights = torch.softmax(attention_scores, dim=1)
        context = torch.bmm(attention_weights.unsqueeze(1), encoder_outputs).squeeze(1)
        return context

class BiLSTMWithAttention(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(BiLSTMWithAttention, self).__init__()
        self.embedding = nn.Embedding(input_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size, bidirectional=True)
        self.attention = Attention(hidden_size * 2)
        self.fc = nn.Linear(hidden_size * 2, num_classes)

    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, _ = self.lstm(embedded)
        context = self.attention(lstm_out)
        output = self.fc(context)
        return output

class TextClassifier:
    def __init__(self, model_save_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = ElectraTokenizer.from_pretrained("monologg/koelectra-base-discriminator", use_fast=False)
        self.model = None
        self.load_model(model_save_path)

    def load_model(self, model_save_path):
        self.model = BiLSTMWithAttention(input_size=len(self.tokenizer), hidden_size=256, num_classes=2)
        self.model.load_state_dict(torch.load(model_save_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

    def classify_text(self, text):
        encoding = self.tokenizer(text, truncation=True, padding=True, return_tensors="pt")
        input_ids = encoding['input_ids'].to(self.device)
        with torch.no_grad():
            outputs = self.model(input_ids)
            probabilities = torch.softmax(outputs, dim=1).tolist()[0]

        label_names = ['Label 0', 'Label 1']
        label_probabilities = {label: prob for label, prob in zip(label_names, probabilities)}
        return label_probabilities
