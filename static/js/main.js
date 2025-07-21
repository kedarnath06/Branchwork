/**
 * Bangla Sentiment Analysis - Main JavaScript
 * Enhanced functionality with animations and interactions
 */

class SentimentAnalyzer {
    constructor() {
        this.apiUrl = '/api/analyze/';
        this.isAnalyzing = false;
        this.lastResult = null;
        
        this.initializeElements();
        this.bindEvents();
        this.setupAnimations();
        this.setupAccessibility();
    }

    initializeElements() {
        // Form elements
        this.form = document.getElementById('sentimentForm');
        this.textInput = document.getElementById('textInput');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        
        // Result elements
        this.loading = document.getElementById('loading');
        this.analysisResult = document.getElementById('analysisResult');
        
        // Circle elements
        this.positiveCircle = document.getElementById('positiveCircle');
        this.neutralCircle = document.getElementById('neutralCircle');
        this.negativeCircle = document.getElementById('negativeCircle');
        
        // Percentage elements
        this.positivePercent = document.getElementById('positivePercent');
        this.neutralPercent = document.getElementById('neutralPercent');
        this.negativePercent = document.getElementById('negativePercent');
        
        // Final prediction
        this.finalPrediction = document.getElementById('finalPrediction');
        
        // Additional elements
        this.closeIcon = document.querySelector('.close-icon');
    }

    bindEvents() {
        // Form submission
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Input validation
        this.textInput.addEventListener('input', () => this.validateInput());
        this.textInput.addEventListener('paste', () => {
            setTimeout(() => this.validateInput(), 100);
        });
        
        // Close button
        if (this.closeIcon) {
            this.closeIcon.addEventListener('click', () => this.clearResults());
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));
        
        // Circle interactions
        this.setupCircleInteractions();
        
        // Auto-resize textarea
        this.textInput.addEventListener('input', () => this.autoResizeTextarea());
    }

    setupAnimations() {
        // Intersection Observer for animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        });

        // Observe elements for animation
        document.querySelectorAll('.input-section, .output-section').forEach(el => {
            observer.observe(el);
        });
    }

    setupAccessibility() {
        // Add ARIA labels
        this.textInput.setAttribute('aria-label', 'Enter Bangla text for sentiment analysis');
        this.analyzeBtn.setAttribute('aria-label', 'Analyze sentiment of entered text');
        
        // Add role attributes
        this.analysisResult.setAttribute('role', 'region');
        this.analysisResult.setAttribute('aria-label', 'Sentiment analysis results');
        
        // Setup screen reader announcements
        this.setupScreenReaderAnnouncements();
    }

    setupScreenReaderAnnouncements() {
        // Create announcement element for screen readers
        this.announcement = document.createElement('div');
        this.announcement.setAttribute('aria-live', 'polite');
        this.announcement.setAttribute('aria-atomic', 'true');
        this.announcement.className = 'sr-only';
        document.body.appendChild(this.announcement);
    }

    setupCircleInteractions() {
        [this.positiveCircle, this.neutralCircle, this.negativeCircle].forEach(circle => {
            if (circle) {
                circle.addEventListener('click', () => this.showCircleDetail(circle));
                circle.setAttribute('tabindex', '0');
                circle.setAttribute('role', 'button');
                
                circle.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        this.showCircleDetail(circle);
                    }
                });
            }
        });
    }

    validateInput() {
        const text = this.textInput.value.trim();
        const isValid = text.length > 0;
        
        this.analyzeBtn.disabled = !isValid || this.isAnalyzing;
        
        // Update button text based on validation
        if (!isValid && !this.isAnalyzing) {
            this.analyzeBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Enter Text';
        } else if (!this.isAnalyzing) {
            this.analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Check';
        }
        
        // Character count (optional)
        this.updateCharacterCount(text.length);
        
        return isValid;
    }

    updateCharacterCount(count) {
        // Optional: Show character count
        let counter = document.getElementById('charCounter');
        if (!counter) {
            counter = document.createElement('div');
            counter.id = 'charCounter';
            counter.className = 'char-counter';
            this.textInput.parentNode.appendChild(counter);
        }
        
        counter.textContent = `${count} characters`;
        counter.style.color = count > 500 ? '#ef4444' : '#6b7280';
    }

    autoResizeTextarea() {
        this.textInput.style.height = 'auto';
        this.textInput.style.height = Math.max(180, this.textInput.scrollHeight) + 'px';
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        if (!this.validateInput() || this.isAnalyzing) {
            return;
        }
        
        const text = this.textInput.value.trim();
        
        try {
            await this.analyzeSentiment(text);
        } catch (error) {
            this.handleError(error);
        }
    }

    async analyzeSentiment(text) {
        this.isAnalyzing = true;
        this.showLoading();
        
        try {
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({ text })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                this.lastResult = data;
                this.displayResults(data);
                this.announceResults(data);
            } else {
                throw new Error(data.message || 'Analysis failed');
            }
            
        } catch (error) {
            console.error('Analysis error:', error);
            this.handleError(error);
        } finally {
            this.isAnalyzing = false;
            this.hideLoading();
        }
    }

    showLoading() {
        this.loading.classList.add('show');
        this.analysisResult.classList.remove('show');
        
        this.analyzeBtn.disabled = true;
        this.analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        
        // Add loading state to input
        this.textInput.style.opacity = '0.7';
        this.textInput.disabled = true;
    }

    hideLoading() {
        this.loading.classList.remove('show');
        
        this.analyzeBtn.disabled = false;
        this.analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Check';
        
        // Remove loading state from input
        this.textInput.style.opacity = '1';
        this.textInput.disabled = false;
    }

    displayResults(data) {
        const { probabilities, sentiment, confidence } = data;
        
        // Update percentages with animation
        this.animatePercentage(this.positivePercent, probabilities.positive);
        this.animatePercentage(this.neutralPercent, probabilities.neutral);
        this.animatePercentage(this.negativePercent, probabilities.negative);
        
        // Update circular progress with animation
        setTimeout(() => {
            this.updateCircularProgress('positiveCircle', probabilities.positive);
            this.updateCircularProgress('neutralCircle', probabilities.neutral);
            this.updateCircularProgress('negativeCircle', probabilities.negative);
        }, 200);
        
        // Update final prediction
        this.finalPrediction.textContent = data.model_analysis;
        this.finalPrediction.className = `prediction-${sentiment}`;
        
        // Show results with animation
        setTimeout(() => {
            this.analysisResult.classList.add('show');
            this.highlightDominantSentiment(sentiment);
        }, 300);
    }

    animatePercentage(element, targetValue) {
        const startValue = 0;
        const duration = 1000;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const currentValue = startValue + (targetValue - startValue) * this.easeOutCubic(progress);
            element.textContent = Math.round(currentValue) + '%';
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }

    updateCircularProgress(elementId, percentage) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.setProperty('--percentage', percentage + '%');
            
            // Add pulse animation for high confidence
            if (percentage > 70) {
                element.classList.add('high-confidence');
                setTimeout(() => element.classList.remove('high-confidence'), 2000);
            }
        }
    }

    highlightDominantSentiment(sentiment) {
        // Remove previous highlights
        document.querySelectorAll('.sentiment-circle').forEach(circle => {
            circle.classList.remove('dominant');
        });
        
        // Add highlight to dominant sentiment
        const dominantCircle = document.querySelector(`.circle.${sentiment}`);
        if (dominantCircle) {
            dominantCircle.closest('.sentiment-circle').classList.add('dominant');
        }
    }

    showCircleDetail(circle) {
        const sentiment = circle.classList.contains('positive') ? 'positive' :
                         circle.classList.contains('neutral') ? 'neutral' : 'negative';
        
        if (!this.lastResult) return;
        
        const percentage = this.lastResult.probabilities[sentiment];
        const message = this.getDetailedMessage(sentiment, percentage);
        
        this.showTooltip(circle, message);
    }

    getDetailedMessage(sentiment, percentage) {
        const confidenceLevel = percentage > 70 ? 'High' : 
                               percentage > 40 ? 'Medium' : 'Low';
        
        return `${sentiment.charAt(0).toUpperCase() + sentiment.slice(1)} Sentiment\n${percentage}% confidence\n${confidenceLevel} certainty`;
    }

    showTooltip(element, message) {
        // Remove existing tooltip
        const existingTooltip = document.querySelector('.custom-tooltip');
        if (existingTooltip) {
            existingTooltip.remove();
        }
        
        // Create new tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'custom-tooltip';
        tooltip.textContent = message;
        
        document.body.appendChild(tooltip);
        
        // Position tooltip
        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
        
        // Auto-remove tooltip
        setTimeout(() => {
            if (tooltip.parentNode) {
                tooltip.remove();
            }
        }, 3000);
    }

    announceResults(data) {
        const { sentiment, confidence } = data;
        const message = `Analysis complete. Sentiment is ${sentiment} with ${confidence}% confidence.`;
        
        this.announcement.textContent = message;
        
        // Also show a brief notification
        this.showNotification(message, 'success');
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Auto-remove
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    clearResults() {
        this.analysisResult.classList.remove('show');
        this.lastResult = null;
        
        // Reset circles
        ['positiveCircle', 'neutralCircle', 'negativeCircle'].forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.style.setProperty('--percentage', '0%');
            }
        });
        
        // Reset percentages
        [this.positivePercent, this.neutralPercent, this.negativePercent].forEach(el => {
            if (el) el.textContent = '0%';
        });
        
        // Clear highlights
        document.querySelectorAll('.sentiment-circle').forEach(circle => {
            circle.classList.remove('dominant');
        });
        
        this.showNotification('Results cleared', 'info');
    }

    handleError(error) {
        console.error('Error:', error);
        
        let message = 'An error occurred while analyzing the text. Please try again.';
        
        if (error.message.includes('Failed to fetch')) {
            message = 'Network error. Please check your connection and try again.';
        } else if (error.message.includes('HTTP')) {
            message = 'Server error. Please try again later.';
        }
        
        this.showNotification(message, 'error');
        this.announcement.textContent = message;
    }

    handleKeyboardShortcuts(e) {
        // Ctrl/Cmd + Enter to analyze
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (!this.isAnalyzing && this.validateInput()) {
                this.form.dispatchEvent(new Event('submit'));
            }
        }
        
        // Escape to clear results
        if (e.key === 'Escape') {
            this.clearResults();
        }
    }

    getCsrfToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return decodeURIComponent(value);
            }
        }
        return '';
    }

    easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
    }
}

// Utility Functions
function addCustomStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .char-counter {
            font-size: 12px;
            color: #6b7280;
            text-align: right;
            margin-top: 5px;
        }
        
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            transform: translateX(400px);
            transition: transform 0.3s ease;
        }
        
        .notification.show {
            transform: translateX(0);
        }
        
        .notification-success {
            background: #10b981;
        }
        
        .notification-error {
            background: #ef4444;
        }
        
        .notification-info {
            background: #3b82f6;
        }
        
        .custom-tooltip {
            position: absolute;
            background: #1f2937;
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 12px;
            white-space: pre-line;
            z-index: 1000;
            animation: fadeIn 0.3s ease;
        }
        
        .custom-tooltip::after {
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 5px solid transparent;
            border-top-color: #1f2937;
        }
        
        .sentiment-circle.dominant {
            transform: scale(1.1);
            filter: brightness(1.1);
        }
        
        .circle.high-confidence {
            animation: pulse 0.5s ease-in-out;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .prediction-positive {
            color: var(--success-color, #10b981);
        }
        
        .prediction-negative {
            color: var(--danger-color, #ef4444);
        }
        
        .prediction-neutral {
            color: var(--warning-color, #f59e0b);
        }
        
        .animate-in {
            animation: slideInUp 0.6s ease-out;
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    addCustomStyles();
    
    // Initialize the sentiment analyzer
    window.sentimentAnalyzer = new SentimentAnalyzer();
    
    // Add loading state management
    window.addEventListener('beforeunload', () => {
        if (window.sentimentAnalyzer && window.sentimentAnalyzer.isAnalyzing) {
            return 'Analysis in progress. Are you sure you want to leave?';
        }
    });
    
    console.log('🚀 Bangla Sentiment Analysis initialized successfully!');
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SentimentAnalyzer;
}