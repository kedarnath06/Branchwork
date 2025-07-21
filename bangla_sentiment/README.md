# Bangla Sentiment Analysis Application

A real-time sentiment analysis application for Bangla text using Django REST Framework and Machine Learning. The application features a modern web interface that analyzes Bangla text and provides sentiment predictions with probability distributions.

## Features

- **Real-time Sentiment Analysis**: Analyze Bangla text in real-time
- **Three Sentiment Categories**: Positive, Negative, and Neutral
- **Probability Distribution**: Shows percentage breakdown for each sentiment
- **Modern UI**: Beautiful, responsive web interface
- **REST API**: JSON-based API for programmatic access
- **Text Preprocessing**: Handles Bangla text preprocessing including stopword removal

## Architecture

The application consists of three main components:

1. **Machine Learning Model**: Currently uses a TF-IDF + Logistic Regression model (can be replaced with CNN)
2. **Backend API**: Django REST Framework handling requests and model predictions
3. **Frontend Interface**: Modern web UI for user interaction

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd bangla_sentiment
```

2. **Create and activate virtual environment**:
```bash
python3 -m venv bangla_sentiment_env
source bangla_sentiment_env/bin/activate  # On Windows: bangla_sentiment_env\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run database migrations**:
```bash
python manage.py migrate
```

5. **Start the development server**:
```bash
python manage.py runserver
```

6. **Access the application**:
   - Web Interface: http://localhost:8000/
   - API Endpoint: http://localhost:8000/api/analyze/

## API Usage

### Analyze Sentiment

**Endpoint**: `POST /api/analyze/`

**Request Body**:
```json
{
    "text": "আমি এই পণ্যটি খুবই পছন্দ করেছি।"
}
```

**Response**:
```json
{
    "text": "আমি এই পণ্যটি খুবই পছন্দ করেছি।",
    "sentiment": "positive",
    "probabilities": {
        "positive": 85.5,
        "negative": 10.2,
        "neutral": 4.3
    },
    "confidence": 85.5,
    "model_analysis": "Positive",
    "success": true
}
```

### API Information

**Endpoint**: `GET /api/analyze/`

Returns API documentation and usage information.

## Model Information

### Current Implementation
- **Algorithm**: TF-IDF + Logistic Regression
- **Language**: Bangla
- **Categories**: Positive, Negative, Neutral
- **Preprocessing**: Stopword removal, text normalization

### Replacing with CNN Model

To use the actual CNN model mentioned in the requirements:

1. Place your trained model file at: `sentiment_analyzer/models/bangla_sentiment_model_all.h5`
2. Place your tokenizer file at: `sentiment_analyzer/models/tokenizer_all.pkl`
3. Update the `_load_or_create_model()` method in `ml_model.py` to load TensorFlow/Keras models

Example implementation for CNN model loading:
```python
import tensorflow as tf
import pickle

# In _load_or_create_model method:
if os.path.exists(model_path) and os.path.exists(tokenizer_path):
    self.model = tf.keras.models.load_model(model_path)
    with open(tokenizer_path, 'rb') as f:
        self.tokenizer = pickle.load(f)
    self.is_loaded = True
```

## Project Structure

```
bangla_sentiment/
├── bangla_sentiment/          # Django project settings
│   ├── __init__.py
│   ├── settings.py           # Django configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py
├── sentiment_analyzer/        # Django app
│   ├── __init__.py
│   ├── ml_model.py          # ML model handler
│   ├── views.py             # API views
│   ├── urls.py              # App URL routing
│   └── models/              # (Create this for model files)
├── templates/
│   └── index.html           # Frontend interface
├── static/                  # Static files (CSS, JS)
├── requirements.txt         # Python dependencies
├── manage.py               # Django management script
└── README.md
```

## Usage Examples

### Web Interface
1. Open http://localhost:8000/ in your browser
2. Enter Bangla text in the input field
3. Click "Check" to analyze sentiment
4. View results with probability distributions

### cURL Example
```bash
curl -X POST http://localhost:8000/api/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"text": "এটি একটি দুর্দান্ত পণ্য!"}'
```

### Python Example
```python
import requests

response = requests.post(
    'http://localhost:8000/api/analyze/',
    json={'text': 'আমি খুশি!'}
)
result = response.json()
print(f"Sentiment: {result['sentiment']}")
print(f"Confidence: {result['confidence']}%")
```

## Development

### Adding New Features
1. Extend the `BanglaSentimentAnalyzer` class in `ml_model.py`
2. Update API views in `views.py`
3. Modify frontend in `templates/index.html`

### Testing
```bash
python manage.py test
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Technical Details

### Text Preprocessing
- Removes special characters
- Normalizes whitespace
- Filters out Bangla stopwords
- Handles Unicode Bangla text (U+0980-U+09FF)

### Model Features
- **Input**: Raw Bangla text
- **Output**: Sentiment probabilities and prediction
- **Preprocessing**: Stopword removal, tokenization
- **Vectorization**: TF-IDF (1-2 grams)
- **Classification**: Logistic Regression

### Security Features
- CORS enabled for cross-origin requests
- CSRF protection
- Input validation and sanitization

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

**Developed by**: Saiful Islam Auny
**Year**: 2025
**Framework**: Django REST Framework
**Frontend**: Modern HTML5/CSS3/JavaScript

## Support

For issues and questions:
- Create an issue on GitHub
- Contact the developer through social media links
- Check the API documentation at `/api/analyze/`

---

*Note: The current implementation uses a demo model. For production use, replace with a trained CNN model as described in the documentation.*