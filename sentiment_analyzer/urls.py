from django.urls import path
from . import views

app_name = 'sentiment_analyzer'

urlpatterns = [
    path('', views.home, name='home'),
    path('analyze/', views.analyze_sentiment, name='analyze_sentiment'),
    path('model-status/', views.model_status, name='model_status'),
]