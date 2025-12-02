import nltk

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from deep_translator import GoogleTranslator
from langdetect import detect
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import warnings
import os

warnings.filterwarnings("ignore")


#  Preprocessing Class

class PreProcessText:
    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        self.stemmer = PorterStemmer()

    def to_lowercase(self, text=''):
        return text.lower()

    def remove_punctuation(self, text=''):
        return ''.join([c for c in text if c not in string.punctuation])

    def tokenize(self, text=''):
        return nltk.word_tokenize(text)

    def remove_stopwords(self, tokens):
        return [t for t in tokens if t not in self.stop_words]

    def stem_words(self, tokens):
        return [self.stemmer.stem(t) for t in tokens]

    def full_preprocess(self, text=''):
        text = self.to_lowercase(text)
        text = self.remove_punctuation(text)
        tokens = self.tokenize(text)
        tokens = self.remove_stopwords(tokens)
        tokens = self.stem_words(tokens)
        return " ".join(tokens)


#  Keyword booster

scam_keywords = [
    "unusual activity", "account restricted", "verify identity", "confirm identity",
    "bank account", "frozen card", "blocked account", "send information",
    "update your data", "win", "prize", "money", "transfer", "bank",
    "urgent", "otp", "code", "identity", "personal info"
]

def keyword_boost_score(text):
    score = 0
    for kw in scam_keywords:
        if kw.lower() in text.lower():
            score += 1
    return score


# Load Model and Vectorizer after initaiting them in the notebook

try:
    base_path = os.path.dirname(__file__)
    tfidf = pickle.load(open(os.path.join(base_path, "tfidf_final.pkl"), "rb"))
    model = pickle.load(open(os.path.join(base_path, "etc_model_final.pkl"), "rb"))
except Exception as e:
    raise RuntimeError(f"Failed to load ML model or TF-IDF: {e}")


# FastAPI Setup

app = FastAPI(title="Scam Detection API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow requests from any origin (for testing)
    allow_methods=["*"],  # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"]   # allow all headers
)
class MessageRequest(BaseModel):
    message: str


# Routes api endpoint the frist one is for checking if the connection is up and the seconde to classfiy
@app.get("/")
def home():
    return {"message": "Scam Detection API is running."}


@app.post("/predict")
def predict(request: MessageRequest):
    msg = request.message.strip()

    if not msg:
        raise HTTPException(status_code=400, detail="Empty message received.")

    try:
        # Detect language
        lang = detect(msg)

        # Translate if Arabic
        if lang == "ar":
            translated = GoogleTranslator(source='ar', target='en').translate(msg)
        else:
            translated = msg

        # Preprocess
        preprocess = PreProcessText()
        processed = preprocess.full_preprocess(translated)

        # Vectorize
        vector_input = tfidf.transform([processed])

        # Model prediction
        model_pred = model.predict(vector_input)[0]    # 0 scam, 1 not scam
        model_prob = model.predict_proba(vector_input).max()

        # Apply Keyword Boost
        boost = keyword_boost_score(translated)
        final_pred = 0 if boost >= 2 else model_pred

        return {
            "original_message": msg,
            "detected_language": lang,
            "translated_message": translated if lang == "ar" else None,
            "model_prediction": "scam" if model_pred == 0 else "not scam",
            "final_prediction": "scam" if final_pred == 0 else "not scam",
            "confidence": float(model_prob),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
