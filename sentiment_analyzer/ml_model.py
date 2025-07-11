"""
Machine Learning model for Bangla sentiment analysis.
This is a mock implementation that simulates a trained CNN model behavior.
In production, this would load the actual bangla_sentiment_model_all.h5 and tokenizer_all.pkl files.
"""

import re
import random
from typing import Dict, List


class BanglaSentimentAnalyzer:
    """
    Mock CNN-based sentiment analyzer for Bangla text.
    Simulates the behavior of a trained model that would classify text into
    Positive, Negative, and Neutral sentiments.
    """
    
    def __init__(self):
        self.model_loaded = False
        self.tokenizer = None
        self.max_length = 100
        
        # Mock Bangla stopwords (in a real implementation, this would be comprehensive)
        self.bangla_stopwords = [
            'এই', 'যে', 'এবং', 'বা', 'কিন্তু', 'হয়', 'হয়েছে', 'করা', 'করে',
            'এর', 'তার', 'তাদের', 'আমি', 'আমার', 'তুমি', 'তোমার', 'সে', 'তার'
        ]
        
        # Mock positive and negative word indicators
        self.positive_indicators = [
            'ভালো', 'সুন্দর', 'চমৎকার', 'দুর্দান্ত', 'অসাধারণ', 'খুশি', 'আনন্দ',
            'ভালোবাসা', 'গর্বিত', 'সফল', 'জয়', 'বিজয়'
        ]
        
        self.negative_indicators = [
            'খারাপ', 'বিরক্তিকর', 'দুঃখ', 'রাগ', 'ক্ষোভ', 'হতাশা', 'ব্যর্থ',
            'অপছন্দ', 'ভয়', 'চিন্তা', 'কষ্ট', 'বিপদ'
        ]
        
        self.load_model()
    
    def load_model(self):
        """
        Mock model loading function.
        In production, this would load:
        - bangla_sentiment_model_all.h5 (CNN model)
        - tokenizer_all.pkl (tokenizer)
        """
        print("Loading Bangla sentiment analysis model...")
        # Simulate model loading time
        self.model_loaded = True
        print("Model loaded successfully!")
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess Bangla text for sentiment analysis.
        """
        if not text:
            return ""
        
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters except Bangla characters and basic punctuation
        text = re.sub(r'[^\u0980-\u09FF\s\.,!?]', '', text)
        
        # Remove stopwords (simplified approach)
        words = text.split()
        filtered_words = [word for word in words if word not in self.bangla_stopwords]
        
        return ' '.join(filtered_words)
    
    def tokenize_and_pad(self, text: str) -> List[int]:
        """
        Mock tokenization and padding function.
        In production, this would use the actual tokenizer.
        """
        # Simple mock tokenization
        words = text.split()
        # Convert to mock integer tokens (for simulation)
        tokens = [hash(word) % 10000 for word in words]
        
        # Pad to max_length
        if len(tokens) < self.max_length:
            tokens.extend([0] * (self.max_length - len(tokens)))
        else:
            tokens = tokens[:self.max_length]
        
        return tokens
    
    def predict_sentiment(self, text: str) -> Dict[str, float]:
        """
        Predict sentiment for given Bangla text.
        Returns probabilities for Positive, Negative, and Neutral sentiments.
        """
        if not self.model_loaded:
            raise Exception("Model not loaded!")
        
        if not text or text.strip() == "":
            return {
                'positive': 0.33,
                'negative': 0.33,
                'neutral': 0.34
            }
        
        # Preprocess the text
        processed_text = self.preprocess_text(text)
        
        # Mock sentiment analysis based on keywords
        positive_score = 0.2  # Base score
        negative_score = 0.2  # Base score
        neutral_score = 0.6   # Base score
        
        words = processed_text.lower().split()
        
        # Check for positive indicators
        for word in words:
            if any(pos_word in word for pos_word in self.positive_indicators):
                positive_score += 0.3
        
        # Check for negative indicators
        for word in words:
            if any(neg_word in word for neg_word in self.negative_indicators):
                negative_score += 0.3
        
        # Add some randomness to simulate model uncertainty
        positive_score += random.uniform(-0.1, 0.1)
        negative_score += random.uniform(-0.1, 0.1)
        neutral_score += random.uniform(-0.1, 0.1)
        
        # Normalize scores
        total = positive_score + negative_score + neutral_score
        
        return {
            'positive': round(positive_score / total, 3),
            'negative': round(negative_score / total, 3),
            'neutral': round(neutral_score / total, 3)
        }
    
    def get_final_prediction(self, probabilities: Dict[str, float]) -> str:
        """
        Get the final sentiment prediction based on highest probability.
        """
        return max(probabilities, key=probabilities.get).title()


# Global model instance
sentiment_model = BanglaSentimentAnalyzer()