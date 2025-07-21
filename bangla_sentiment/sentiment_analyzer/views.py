from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import logging

from .ml_model import get_sentiment_analyzer

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class AnalyzeSentimentView(APIView):
    """
    API endpoint for analyzing sentiment of Bangla text
    """
    
    def post(self, request):
        """
        Analyze sentiment of the provided Bangla text
        
        Expected JSON payload:
        {
            "text": "Bangla text to analyze"
        }
        
        Returns:
        {
            "text": "input text",
            "sentiment": "positive/negative/neutral",
            "probabilities": {
                "positive": 85.5,
                "negative": 10.2,
                "neutral": 4.3
            },
            "confidence": 85.5,
            "model_analysis": "Positive"
        }
        """
        try:
            # Parse JSON data
            if hasattr(request, 'data') and request.data:
                data = request.data
            else:
                data = json.loads(request.body.decode('utf-8'))
            
            # Extract text from request
            text = data.get('text', '').strip()
            
            if not text:
                return Response({
                    'error': 'Text is required',
                    'message': 'Please provide text in the request body'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get sentiment analyzer
            analyzer = get_sentiment_analyzer()
            
            # Perform sentiment analysis
            result = analyzer.predict_sentiment(text)
            
            # Format response
            response_data = {
                'text': text,
                'sentiment': result['prediction'],
                'probabilities': result['probabilities'],
                'confidence': result['confidence'],
                'model_analysis': result['prediction'].capitalize(),
                'success': True
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except json.JSONDecodeError:
            return Response({
                'error': 'Invalid JSON',
                'message': 'Please provide valid JSON data'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return Response({
                'error': 'Internal server error',
                'message': 'An error occurred while processing your request'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        """
        Get API information
        """
        return Response({
            'message': 'Bangla Sentiment Analysis API',
            'version': '1.0',
            'endpoints': {
                'analyze': '/api/analyze/ (POST)',
            },
            'usage': {
                'method': 'POST',
                'content_type': 'application/json',
                'body': {
                    'text': 'Your Bangla text here'
                }
            }
        }, status=status.HTTP_200_OK)
