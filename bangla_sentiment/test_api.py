#!/usr/bin/env python3
"""
Test script for Bangla Sentiment Analysis API
Demonstrates the functionality with various text examples
"""

import requests
import json
import time

def test_sentiment_analysis():
    """Test the sentiment analysis API with various examples"""
    
    base_url = "http://localhost:8000/api/analyze/"
    
    # Test cases with different sentiments
    test_cases = [
        {
            "text": "আমি এই পণ্যটি খুব পছন্দ করেছি। এটি দুর্দান্ত!",
            "expected": "positive",
            "description": "Positive sentiment - Product appreciation"
        },
        {
            "text": "এটি খুবই খারাপ এবং ভয়ানক অভিজ্ঞতা ছিল।",
            "expected": "negative", 
            "description": "Negative sentiment - Bad experience"
        },
        {
            "text": "এটি সাধারণ মানের। কিছু ভাল আর কিছু খারাপ।",
            "expected": "neutral",
            "description": "Neutral sentiment - Mixed opinion"
        },
        {
            "text": "চমৎকার সেবা! আমি খুশি।",
            "expected": "positive",
            "description": "Positive sentiment - Service appreciation"
        },
        {
            "text": "আমি হতাশ। এটি আমার প্রত্যাশা পূরণ করেনি।",
            "expected": "negative",
            "description": "Negative sentiment - Disappointment"
        }
    ]
    
    print("🚀 Testing Bangla Sentiment Analysis API")
    print("=" * 50)
    
    # Test API info endpoint
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ API Info endpoint working")
            print(f"   Response: {response.json()['message']}")
        else:
            print("❌ API Info endpoint failed")
            return
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("   Make sure the Django server is running: python manage.py runserver")
        return
    
    print()
    print("🧪 Testing Sentiment Analysis...")
    print("-" * 50)
    
    # Test sentiment analysis
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print(f"Text: {test_case['text']}")
        
        try:
            response = requests.post(
                base_url,
                json={"text": test_case['text']},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                sentiment = result['sentiment']
                confidence = result['confidence']
                probabilities = result['probabilities']
                
                print(f"📊 Result: {sentiment.upper()} ({confidence}% confidence)")
                print(f"   Positive: {probabilities['positive']}%")
                print(f"   Neutral:  {probabilities['neutral']}%") 
                print(f"   Negative: {probabilities['negative']}%")
                
                # Check if prediction matches expected (optional)
                if sentiment == test_case['expected']:
                    print("✅ Prediction matches expected")
                else:
                    print(f"⚠️  Expected {test_case['expected']}, got {sentiment}")
                    
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(0.5)  # Small delay between requests
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")
    print("\n📝 Usage Examples:")
    print("   Web Interface: http://localhost:8000/")
    print("   API Endpoint:  http://localhost:8000/api/analyze/")
    print("")
    print("   Example curl command:")
    print('   curl -X POST http://localhost:8000/api/analyze/ \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"text": "আমি খুশি!"}\'')

if __name__ == "__main__":
    test_sentiment_analysis()