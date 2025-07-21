from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.AnalyzeSentimentView.as_view(), name='analyze_sentiment'),
]