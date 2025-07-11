from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .ml_model import sentiment_model
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
def analyze_sentiment(request):
    """
    API endpoint to analyze sentiment of Bangla text.
    
    POST /analyze/
    
    Request body:
    {
        "text": "বাংলা টেক্সট এখানে লিখুন"
    }
    
    Response:
    {
        "text": "input text",
        "probabilities": {
            "positive": 0.75,
            "negative": 0.15,
            "neutral": 0.10
        },
        "prediction": "Positive",
        "status": "success"
    }
    """
    try:
        # Get text from request
        text = request.data.get('text', '').strip()
        
        if not text:
            return Response({
                'error': 'No text provided',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if text is too long (optional validation)
        if len(text) > 1000:
            return Response({
                'error': 'Text is too long. Maximum 1000 characters allowed.',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Analyze sentiment using the model
        probabilities = sentiment_model.predict_sentiment(text)
        prediction = sentiment_model.get_final_prediction(probabilities)
        
        # Prepare response
        response_data = {
            'text': text,
            'probabilities': probabilities,
            'prediction': prediction,
            'status': 'success'
        }
        
        logger.info(f"Sentiment analysis completed for text: {text[:50]}...")
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        return Response({
            'error': 'Internal server error occurred during sentiment analysis',
            'status': 'error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def home(request):
    """
    Home page view that renders the main sentiment analysis interface.
    """
    return render(request, 'sentiment_analyzer/index.html')


@api_view(['GET'])
def model_status(request):
    """
    API endpoint to check model status.
    
    GET /model-status/
    """
    try:
        return Response({
            'model_loaded': sentiment_model.model_loaded,
            'status': 'success' if sentiment_model.model_loaded else 'model_not_loaded'
        })
    except Exception as e:
        return Response({
            'error': str(e),
            'status': 'error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
