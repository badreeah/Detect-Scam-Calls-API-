# Scam Call Detection API

A machine learning-powered REST API that detects fraudulent phone call messages in real-time. The system uses Natural Language Processing (NLP) and Extra Trees Classifier to identify scam patterns in text messages, supporting both English and Arabic languages.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Running the API](#running-the-api)
- [API Endpoints](#api-endpoints)
- [Testing with Postman](#testing-with-postman)
- [Model Details](#model-details)
- [Dataset](#dataset)
- [What This Project Solves](#What-This-Project-Solves)

---

## Overview

This project provides a FastAPI-based REST API hosted on Railway that analyzes phone call messages and determines whether they are fraudulent or legitimate. The system combines machine learning predictions with keyword-based boosting to achieve high accuracy in scam detection.

**Key Capabilities:**

- Real-time scam message detection
- Multi-language support (English & Arabic)
- Automatic text translation
- Advanced NLP preprocessing
- High accuracy (98%+)
- RESTful API interface

---

## Features

1. **Machine Learning Classification**: Uses Extra Trees Classifier trained on TF-IDF features
2. **Language Detection**: Automatically detects message language
3. **Arabic Translation**: Translates Arabic messages to English for processing
4. **Text Preprocessing**:
   - Lowercasing
   - Punctuation removal
   - Tokenization
   - Stop word removal
   - Stemming
5. **Keyword Boosting**: Enhanced detection using scam-related keywords
6. **SMOTE Balancing**: Model trained on balanced dataset for improved minority class detection
7. **CORS Enabled**: Ready for frontend integration

---

## Project Structure

```
Detect-Scam-Calls-API--main/
│
├── app.py                          # Main FastAPI application , used to upload the API on Railway
├── requirements.txt                # Python dependencies
├── download_nltk.py               # NLTK data downloader script
│
├── MainCall.csv                   # Training dataset (fraud/normal messages)
├── Copy_of_etc_model_(1).ipynb   # Model training notebook
│
├── tfidf_final.pkl               # Final Trained TF-IDF vectorizer (saved after training)
├── etc_model_final.pkl           # Final Trained Extra Trees model (saved after training)
│
└── README.md
```

---

##  Technologies Used

- **Python 3.13**
- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI (Asynchronous Server Gateway Interface) used because FastAPI is not a server by itself it’s a framework. Uvicorn provides the actual server that API.
- **Scikit-learn**: Machine learning library
- **NLTK**: Natural Language Toolkit
- **Deep Translator**: Language translation
- **LangDetect**: Language detection
- **Pandas & NumPy**: Data manipulation
- **Imbalanced-learn**: SMOTE for data balancing keyword boosting function

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Installation

1. **Clone or Download the Repository**

   ```bash
   cd c:\Users\thecu\Downloads\Detect-Scam-Calls-API--main
   ```

2. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK Data**

   ```bash
   python download_nltk.py
   ```

---

## Running the API

### Start the Server : open app.py on PyCharm

Open your terminal (Command Prompt or PowerShell) and run:

```bash
uvicorn app:app --reload
```

**Expected Output:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Access the API

- **Expected Base URL**: `http://127.0.0.1:8000`

---

## API Endpoints

### 1. Health Check

**GET** `/`

**Response:**

```json
{
  "message": "Scam Detection API is running."
}
```

---

### 2. Predict Scam Message

**POST** `/predict`

**Request Body:**

```json
{
  "message": "hello sir, i am ahmed from customer care in 23 hours your bank account will be closed."
}
```

**Response:**

```json
{
  "original_message": "hello sir, i am ahmed from customer care in 23 hours your bank account will be closed.",
  "detected_language": "en",
  "translated_message": null,
  "model_prediction": "scam",
  "final_prediction": "scam",
  "confidence": 0.98
}
```

**Response Fields:**

- `original_message`: The input message
- `detected_language`: Detected language code (en/ar)
- `translated_message`: English translation (if Arabic)
- `model_prediction`: ML model's prediction
- `final_prediction`: Final prediction after keyword boosting
- `confidence`: Model confidence score (0-1)

---

## Testing with Postman

### Step 1: Open Postman

Download and install Postman if you haven't already.

### Step 2: Test Health Check Endpoint

1. Create a new request
2. Set method to **GET**
3. Enter URL: `http://127.0.0.1:8000/`
4. Click **Send**

**Expected Response:**

```json
{
  "message": "Scam Detection API is running."
}
```

---

### Step 3: Test Prediction Endpoint

1. Create a new request
2. Set method to **POST**
3. Enter URL: `http://127.0.0.1:8000/predict`
4. Go to **Body** tab
5. Select **raw** and **JSON**
6. Enter test message:

**Example 1: Normal Message**

```json
{
  "message": "Hey! How are you doing today? Let's meet for coffee tomorrow."
}
```

**Example 2: Arabic Scam Message**

```json
{
  "message": "عزيزي العميل، تم اكتشاف نشاط غير معتاد في حسابك البنكي. يرجى الاتصال فوراً."
}
```

7. Click **Send**




## Model Details

### Algorithm

- **Classifier**: Extra Trees Classifier (Ensemble method)
- **Features**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Max Features**: 3000

### Performance Metrics

- **Accuracy**: 98.22%
- **Precision**: 98.15%
- **Recall (Scam)**: 99.90%
- **Recall (Normal)**: 84.03%

### Data Preprocessing

1. **Lowercase conversion**
2. **Punctuation removal**
3. **Tokenization** (NLTK word_tokenize)
4. **Stop words removal** (English stopwords)
5. **Stemming** (Porter Stemmer)

### Balancing Technique

- **SMOTE** (Synthetic Minority Over-sampling Technique) was applied to handle class imbalance

### Scam Keywords Boost

The system uses keyword matching to enhance detection accuracy. Messages containing 2+ keywords from this list are automatically flagged as scam:

- unusual activity, account restricted, verify identity.
- bank account, frozen card, blocked account.
- win, prize, money, transfer, urgent.
- otp, code, personal info, cvv.

---

## Dataset

### Source

- **File**: `MainCall.csv`
- **Format**: CSV with 2 columns (label, message)


## API Usage Examples

### JavaScript (Fetch)

```javascript
fetch("http://127.0.0.1:8000/predict", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    message: "You won a prize! Call now.",
  }),
})
  .then((response) => response.json())
  .then((data) => console.log(data));
```

---

## What This Project Solves

This API addresses the growing problem of **phone scam fraud** by:

1. **Protecting Users**: Automatically identifies fraudulent messages attempting to steal personal information
2. **Multi-language Support**: Works with both English and Arabic messages
3. **Real-time Detection**: Provides instant analysis through REST API
4. **High Accuracy**: Achieves 98%+ accuracy using advanced ML techniques
5. **Scalable Solution**: Can be integrated into mobile apps, web applications, or messaging platforms

