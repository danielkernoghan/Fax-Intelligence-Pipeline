import torch
from transformers import BertTokenizer, BertForSequenceClassification, pipeline

# Load models
model = BertForSequenceClassification.from_pretrained("PATH")
tokenizer = BertTokenizer.from_pretrained("PATH")
nlp = pipeline("document-question-answering", model="impira/layoutlm-document-qa")

health_number_questions = [
    "What is the health card number?",
    "What is the health insurance number?",
    "What is the HIN?",
    "What is the HCN?",
    "What is the health insurance #?",
    "What is the health card #?",
    "What is the health number?",
    "What is the health #?"
]

outbreak_questions = [
    "What is the outbreak?",
    "What is the outbreak number?",
    "What is the outbreak #?",
    "What is the OBTK?",
    "What is the OBTK number?",
    "What is the OBTK #?"
]

def predict(text):
    """
    Predicts the class of the given text using a pre-trained model.

    Parameters:
        text (str): The input text to be classified.

    Returns:
        int: The predicted class index.
    """
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(predictions, dim=-1).item()
    return predicted_class
