import os
import re
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

class BanglaSentimentAnalyzer:
    """
    Bangla Sentiment Analysis Model Handler
    
    This class handles the loading and prediction of sentiment for Bangla text.
    For demo purposes, this uses a simple TF-IDF + Logistic Regression model
    that can be easily replaced with a pre-trained CNN model.
    """
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.max_len = 100
        self.is_loaded = False
        
        # Bangla stopwords (basic set)
        self.bangla_stopwords = {
            'এবং', 'বা', 'যে', 'এই', 'সে', 'তার', 'করে', 'করা', 'হয়', 'হয়েছে',
            'থেকে', 'দিয়ে', 'নিয়ে', 'পর', 'আগে', 'পরে', 'উপর', 'নিচে', 'মধ্যে',
            'ভিতর', 'বাহির', 'সাথে', 'ছাড়া', 'জন্য', 'কারণ', 'যদি', 'তাহলে',
            'কিন্তু', 'তবে', 'অথচ', 'তথাপি', 'আর', 'ও', 'কি', 'কী', 'কে', 'কাকে'
        }
        
        # Load or create the model
        self._load_or_create_model()
    
    def _preprocess_text(self, text):
        """
        Preprocess the input text
        """
        if not text:
            return ""
        
        # Remove special characters and normalize
        text = re.sub(r'[^\u0980-\u09FF\s]', '', text)  # Keep only Bangla characters and spaces
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
        text = text.strip()
        
        # Remove stopwords
        words = text.split()
        words = [word for word in words if word not in self.bangla_stopwords]
        
        return ' '.join(words)
    
    def _load_or_create_model(self):
        """
        Load the trained model or create a demo model
        """
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'bangla_sentiment_model_all.h5')
        tokenizer_path = os.path.join(os.path.dirname(__file__), 'models', 'tokenizer_all.pkl')
        
        # For demo purposes, we'll create a simple model
        # In production, you would load the actual CNN model here
        if os.path.exists(model_path) and os.path.exists(tokenizer_path):
            # Load actual trained model (placeholder for now)
            pass
        
        # Create a demo model using sklearn
        self._create_demo_model()
        
    def _create_demo_model(self):
        """
        Create a demo model for demonstration purposes
        """
        # Sample training data for demo
        sample_texts = [
            'এটি একটি খুব ভাল পণ্য',  # Positive
            'আমি এটি পছন্দ করি',        # Positive  
            'চমৎকার সেবা',             # Positive
            'খুবই খারাপ অভিজ্ঞতা',      # Negative
            'এটি ভয়ানক',             # Negative
            'সাধারণ মানের',            # Neutral
            'কিছু ভাল কিছু খারাপ',      # Neutral
        ]
        
        sample_labels = [2, 2, 2, 0, 0, 1, 1]  # 0: Negative, 1: Neutral, 2: Positive
        
        # Preprocess sample texts
        processed_texts = [self._preprocess_text(text) for text in sample_texts]
        
        # Create and train the model
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
            ('classifier', LogisticRegression(random_state=42))
        ])
        
        self.model.fit(processed_texts, sample_labels)
        self.is_loaded = True
    
    def predict_sentiment(self, text):
        """
        Predict sentiment for the given text
        
        Args:
            text (str): Input Bangla text
            
        Returns:
            dict: Dictionary containing probabilities and prediction
        """
        if not self.is_loaded:
            raise Exception("Model not loaded")
        
        if not text or not text.strip():
            return {
                'probabilities': {'negative': 0.33, 'neutral': 0.34, 'positive': 0.33},
                'prediction': 'neutral',
                'confidence': 0.34
            }
        
        # Preprocess the text
        processed_text = self._preprocess_text(text)
        
        if not processed_text:
            return {
                'probabilities': {'negative': 0.33, 'neutral': 0.34, 'positive': 0.33},
                'prediction': 'neutral',
                'confidence': 0.34
            }
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba([processed_text])[0]
        
        # Get the predicted class
        predicted_class = self.model.predict([processed_text])[0]
        
        # Map class indices to sentiment labels
        sentiment_map = {0: 'negative', 1: 'neutral', 2: 'positive'}
        
        # Create result dictionary
        result = {
            'probabilities': {
                'negative': round(float(probabilities[0]) * 100, 2),
                'neutral': round(float(probabilities[1]) * 100, 2),
                'positive': round(float(probabilities[2]) * 100, 2)
            },
            'prediction': sentiment_map[predicted_class],
            'confidence': round(float(max(probabilities)) * 100, 2)
        }
        
        return result

# Global model instance
sentiment_analyzer = None

def get_sentiment_analyzer():
    """
    Get or create the global sentiment analyzer instance
    """
    global sentiment_analyzer
    if sentiment_analyzer is None:
        sentiment_analyzer = BanglaSentimentAnalyzer()
    return sentiment_analyzer