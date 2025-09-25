from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from deep_translator import GoogleTranslator
from langdetect import detect
import pickle
import nltk
from nltk.corpus import stopwords
import string
import warnings
import os

# Ignore warnings
warnings.filterwarnings("ignore")

# -------------------------
# Preprocessing class
# -------------------------
class PreProcessText:
    def remove_punctuation(self, text=''):
        return ''.join([x for x in text if x not in string.punctuation])

    def remove_stopwords(self, text=''):
        return ' '.join([word for word in text.split() if word.lower() not in stopwords.words('english')])

    def token_words(self, text=''):
        message = self.remove_punctuation(text)
        return self.remove_stopwords(message)

# -------------------------
# Load model & vectorizer safely
# -------------------------
try:
    tfidf_path = os.path.join(os.path.dirname(__file__), 'vectorizer2.pkl')
    model_path = os.path.join(os.path.dirname(__file__), 'model2.pkl')
    tfidf = pickle.load(open(tfidf_path, 'rb'))
    prediction_model = pickle.load(open(model_path, 'rb'))
except FileNotFoundError as e:
    raise RuntimeError(f"Model or vectorizer not found: {e}")

# -------------------------
# FastAPI app setup
# -------------------------
app = FastAPI(title="Scam Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Request model
# -------------------------
class MessageRequest(BaseModel):
    message: str

# -------------------------
# Routes
# -------------------------
@app.get("/")
def home():
    return {"message": "✅ Scam Detection API is running. Use POST /predict with JSON {'message': '...'}"}

@app.post("/predict")
def predict(request: MessageRequest):
    input_message = request.message.strip()

    if not input_message:
        raise HTTPException(status_code=400, detail="No input message provided")

    try:
        # Detect language
        lang = detect(input_message)

        # Translate if Arabic
        input_message_en = input_message
        if lang == "ar":
            input_message_en = GoogleTranslator(source='ar', target='en').translate(input_message)

        # Preprocess
        obj = PreProcessText()
        transform_message = obj.remove_punctuation(input_message_en)

        # Vectorize
        vector_input = tfidf.transform([transform_message])

        # Predict
        result = prediction_model.predict(vector_input)[0]
        probability = prediction_model.predict_proba(vector_input).max()

        return {
            "original_message": input_message,
            "detected_language": lang,
            "translated_message": input_message_en if lang == "ar" else None,
            "prediction": "scam" if result == 0 else "not scam",
            "probability": float(probability)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
