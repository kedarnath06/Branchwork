# Bangla Sentiment Analysis Application

A real-time sentiment analysis web application for Bangla text using Django and a CNN-based machine learning model.

## 🌟 Features

- **Real-time Sentiment Analysis**: Analyze Bangla text for positive, negative, and neutral sentiments
- **Modern Web Interface**: Beautiful, responsive UI with real-time results
- **RESTful API**: Django REST Framework powered API endpoints
- **CNN Model Simulation**: Mock implementation of CNN model behavior
- **Progress Visualization**: Interactive charts showing sentiment probabilities
- **Multilingual Support**: Interface supports both Bangla and English

## 🏗️ Architecture

The application follows a three-tier architecture:

### 1. Machine Learning Layer (`sentiment_analyzer/ml_model.py`)
- **BanglaSentimentAnalyzer**: Main model class that simulates CNN behavior
- **Text Preprocessing**: Bangla text cleaning and stopword removal
- **Tokenization**: Mock tokenization and padding for model input
- **Sentiment Prediction**: Returns probabilities for all three sentiment classes

### 2. Backend API Layer (Django + DRF)
- **Django Views**: Handle HTTP requests and responses
- **API Endpoints**:
  - `POST /analyze/` - Main sentiment analysis endpoint
  - `GET /model-status/` - Check model loading status
- **CORS Support**: Enabled for cross-origin requests

### 3. Frontend Layer (HTML + CSS + JavaScript)
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: AJAX-based communication with backend
- **Progress Bars**: Visual representation of sentiment probabilities
- **Error Handling**: User-friendly error messages

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (tested with Python 3.13)
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd bangla-sentiment-analysis
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   - Web Interface: http://localhost:8000/
   - API Endpoint: http://localhost:8000/analyze/

## 🔧 API Usage

### Analyze Sentiment

**Endpoint**: `POST /analyze/`

**Request**:
```json
{
    "text": "এই গেমটি খুবই চমৎকার এবং মজার।"
}
```

**Response**:
```json
{
    "text": "এই গেমটি খুবই চমৎকার এবং মজার।",
    "probabilities": {
        "positive": 0.892,
        "negative": 0.054,
        "neutral": 0.054
    },
    "prediction": "Positive",
    "status": "success"
}
```

### Check Model Status

**Endpoint**: `GET /model-status/`

**Response**:
```json
{
    "model_loaded": true,
    "status": "success"
}
```

## 📁 Project Structure

```
bangla-sentiment-analysis/
├── bangla_sentiment/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── sentiment_analyzer/        # Main application
│   ├── ml_model.py           # Machine learning model
│   ├── views.py              # API views
│   ├── urls.py               # URL routing
│   └── apps.py
├── templates/                 # HTML templates
│   └── sentiment_analyzer/
│       └── index.html        # Main web interface
├── static/                    # Static files (CSS, JS)
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
└── README.md                 # This file
```

## 🎯 User Interaction Workflow

1. **Input**: User enters Bangla text in the web interface
2. **Submission**: Clicks "Analyze Sentiment" button
3. **Processing**: 
   - Frontend sends AJAX request to `/analyze/` endpoint
   - Backend preprocesses the text
   - ML model analyzes sentiment
   - Results returned as JSON
4. **Display**: 
   - Probability bars show sentiment distribution
   - Final prediction highlighted with color coding
   - Model confidence displayed as percentages

## 🔬 Model Details

### Current Implementation
- **Type**: Mock CNN simulation
- **Languages**: Bangla (বাংলা)
- **Classes**: Positive, Negative, Neutral
- **Features**: 
  - Bangla stopword removal
  - Keyword-based sentiment detection
  - Probability normalization

### Production Implementation Notes
In a production environment, this would include:
- **Model File**: `bangla_sentiment_model_all.h5` (TensorFlow/Keras CNN model)
- **Tokenizer**: `tokenizer_all.pkl` (Pickle serialized tokenizer)
- **Training Data**: 536,930 Bangla YouTube comments
- **Architecture**: CNN with embedding layers

## 🧪 Testing the Application

### Web Interface Testing
1. Visit http://localhost:8000/
2. Enter Bangla text examples:
   - Positive: "এই গেমটি অসাধারণ এবং চমৎকার!"
   - Negative: "এটি খুবই খারাপ এবং বিরক্তিকর।"
   - Neutral: "আজ আবহাওয়া ভালো আছে।"

### API Testing with curl
```bash
curl -X POST http://localhost:8000/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"text": "আমি এই সিনেমাটি খুব পছন্দ করেছি।"}'
```

## 🛠️ Development

### Adding New Features
1. **Extend ML Model**: Modify `sentiment_analyzer/ml_model.py`
2. **Add API Endpoints**: Update `sentiment_analyzer/views.py` and `urls.py`
3. **Update Frontend**: Modify `templates/sentiment_analyzer/index.html`

### Configuration
- **Django Settings**: `bangla_sentiment/settings.py`
- **CORS Settings**: Configured for development (allow all origins)
- **Static Files**: Served by WhiteNoise in production

## 📊 Model Performance Notes

The current mock implementation provides:
- **Accuracy**: Simulated based on keyword matching
- **Speed**: Very fast (no actual model inference)
- **Memory**: Low memory footprint

For production deployment with actual CNN model:
- **Expected Accuracy**: ~85-90% on test data
- **Processing Time**: 50-200ms per request
- **Memory Requirements**: 2-4GB RAM recommended

## 🚀 Deployment

### Production Deployment
1. **Environment Variables**:
   ```bash
   export DEBUG=False
   export ALLOWED_HOSTS=yourdomain.com
   ```

2. **Static Files**:
   ```bash
   python manage.py collectstatic
   ```

3. **WSGI Server**:
   ```bash
   gunicorn bangla_sentiment.wsgi:application
   ```

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "bangla_sentiment.wsgi:application"]
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Saiful Islam Auny**
- Email: [your-email@example.com]
- GitHub: [@your-username]
- LinkedIn: [Your LinkedIn Profile]

## 🙏 Acknowledgments

- Thanks to the Bangla NLP community for resources and inspiration
- Django and Django REST Framework communities
- Font Awesome for icons
- All contributors who helped improve this project

---

**Note**: This is a demonstration application. The results may not be 100% accurate and should be used for educational purposes.