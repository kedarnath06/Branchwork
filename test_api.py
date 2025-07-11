#!/usr/bin/env python3
"""
Test script for Bangla Sentiment Analysis API
Demonstrates the functionality with various text examples
"""

import requests
import json
import time

# API base URL
BASE_URL = 'http://localhost:8000'

def test_sentiment_analysis():
    """Test the sentiment analysis API with various Bangla text examples"""
    
    test_cases = [
        {
            'text': 'এই গেমটি অসাধারণ এবং চমৎকার! আমি খুবই খুশি।',
            'expected': 'positive',
            'description': 'Positive text about a game'
        },
        {
            'text': 'এটি খুবই খারাপ এবং বিরক্তিকর। আমি হতাশ।',
            'expected': 'negative',
            'description': 'Negative text expressing disappointment'
        },
        {
            'text': 'আজ আবহাওয়া ভালো আছে। সূর্য উঠেছে।',
            'expected': 'neutral',
            'description': 'Neutral text about weather'
        },
        {
            'text': 'আমি ভালোবাসি এই সুন্দর জায়গাটি।',
            'expected': 'positive',
            'description': 'Positive text expressing love'
        },
        {
            'text': 'দুঃখের কথা, আমার মন খারাপ।',
            'expected': 'negative',
            'description': 'Negative text expressing sadness'
        }
    ]
    
    print("🧪 Testing Bangla Sentiment Analysis API")
    print("=" * 50)
    
    # Test model status first
    try:
        response = requests.get(f'{BASE_URL}/model-status/')
        if response.status_code == 200:
            status_data = response.json()
            print(f"✅ Model Status: {status_data}")
        else:
            print(f"❌ Failed to get model status: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return
    
    print("\n📝 Testing sentiment analysis...")
    print("-" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['description']}")
        print(f"   Text: {test_case['text']}")
        
        try:
            response = requests.post(
                f'{BASE_URL}/analyze/',
                headers={'Content-Type': 'application/json'},
                json={'text': test_case['text']}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"   Prediction: {result['prediction']}")
                print(f"   Probabilities:")
                for sentiment, prob in result['probabilities'].items():
                    print(f"     {sentiment.title()}: {prob:.1%}")
                
                # Check if prediction matches expectation
                actual = result['prediction'].lower()
                expected = test_case['expected']
                if actual == expected:
                    print(f"   ✅ Result matches expectation ({expected})")
                else:
                    print(f"   ⚠️  Result ({actual}) differs from expectation ({expected})")
                    
            else:
                print(f"   ❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(0.5)  # Small delay between requests
    
    print("\n" + "=" * 50)
    print("✅ Testing completed!")

def test_error_handling():
    """Test API error handling"""
    print("\n🔍 Testing error handling...")
    print("-" * 30)
    
    # Test empty text
    try:
        response = requests.post(
            f'{BASE_URL}/analyze/',
            headers={'Content-Type': 'application/json'},
            json={'text': ''}
        )
        print(f"Empty text response: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Error testing empty text: {e}")
    
    # Test very long text
    try:
        long_text = 'অনেক লম্বা টেক্সট ' * 100  # Very long text
        response = requests.post(
            f'{BASE_URL}/analyze/',
            headers={'Content-Type': 'application/json'},
            json={'text': long_text}
        )
        print(f"Long text response: {response.status_code}")
        if response.status_code != 200:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing long text: {e}")

if __name__ == '__main__':
    test_sentiment_analysis()
    test_error_handling()
    
    print("\n🌐 You can also test the web interface at:")
    print(f"   {BASE_URL}/")
    print("\n📖 API Documentation:")
    print(f"   POST {BASE_URL}/analyze/ - Analyze sentiment")
    print(f"   GET  {BASE_URL}/model-status/ - Check model status")