# 🚴‍♂️ Bike Sharing Demand Prediction - Complete End-to-End Data Science Project

A comprehensive data science project that predicts bike sharing demand using machine learning, featuring a modern web interface, REST API, and comprehensive testing suite.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Model Details](#model-details)
- [Testing](#testing)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project models the demand for shared bikes using various independent variables. It helps management understand how demand varies with different features, enabling them to manipulate business strategies to meet demand levels and customer expectations. The model also provides insights into demand dynamics for new markets.

### Business Context
- **Company**: BoomBikes (US bike-sharing provider)
- **Challenge**: Revenue dips due to COVID-19 pandemic
- **Goal**: Understand post-pandemic bike sharing demand patterns
- **Dataset**: Daily bike rental data with weather, seasonal, and temporal features

## ✨ Features

### 🎨 Modern Web Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Forms**: Real-time validation and user feedback
- **Animated Predictions**: Smooth number animations for results
- **Sample Data**: One-click sample data loading for testing
- **Modern UI**: Clean, professional design with gradient backgrounds

### 🔧 Backend API
- **RESTful API**: Clean, well-documented endpoints
- **Input Validation**: Comprehensive data validation
- **Error Handling**: Graceful error responses
- **Health Checks**: System monitoring endpoints
- **Scalable Architecture**: Modular, maintainable code

### 🧪 Comprehensive Testing
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Edge Case Testing**: Boundary value testing
- **API Testing**: Complete endpoint coverage
- **Model Testing**: Prediction accuracy validation

### 📊 Model Insights
- **Linear Regression**: Interpretable coefficients
- **Feature Engineering**: Categorical variable encoding
- **Statistical Analysis**: VIF, p-values, R² scores
- **Performance Metrics**: ~83% accuracy on test data

## 📁 Project Structure

```
Bike-sharing/
├── app.py                 # Flask application and API endpoints
├── test_app.py           # Comprehensive test suite
├── requirements.txt      # Python dependencies
├── setup.py             # Setup and installation script
├── pyproject.toml        # Project configuration
├── README.md            # This file
├── bike.ipynb           # Original Jupyter notebook analysis
├── templates/
│   └── index.html       # Main web interface
├── static/
│   ├── style.css        # Modern CSS styling
│   └── script.js        # Interactive JavaScript
└── logs/                # Application logs (created on run)
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/vannu07/Bike-sharing.git
   cd Bike-sharing
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

### Manual Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run tests**
   ```bash
   python -m pytest test_app.py -v
   ```

3. **Start the application**
   ```bash
   python app.py
   ```

## 💻 Usage

### Web Interface

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:5000`

3. **Fill the form**
   - Select date and time information
   - Enter weather conditions
   - Choose seasonal factors
   - Click "Predict Bike Demand"

4. **View results**
   - See animated prediction results
   - Review model insights
   - Use sample data for testing

### API Usage

#### Predict Bike Demand
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "year": 1,
    "month": "Jul",
    "weekday": "Mon",
    "temperature": 25.0,
    "humidity": 60.0,
    "windspeed": 10.0,
    "weather": "Clear",
    "season": "Summer",
    "holiday": 0,
    "workingday": 1
  }'
```

#### Health Check
```bash
curl http://localhost:5000/health
```

## 📚 API Documentation

### Endpoints

#### `GET /`
- **Description**: Main web interface
- **Response**: HTML page with prediction form

#### `POST /predict`
- **Description**: Predict bike sharing demand
- **Request Body**:
  ```json
  {
    "year": 0|1,           // 0=2018, 1=2019
    "month": "Jan|Feb|...", // Month name
    "weekday": "Mon|Tue|...", // Day of week
    "temperature": float,  // Temperature in °C
    "humidity": float,      // Humidity percentage (0-100)
    "windspeed": float,     // Wind speed in km/h
    "weather": "Clear|Light_rainfall|Thunderstrom",
    "season": "Spring|Summer|Fall|Winter",
    "holiday": 0|1,         // Is holiday
    "workingday": 0|1      // Is working day
  }
  ```
- **Response**:
  ```json
  {
    "prediction": 1234,    // Predicted bike rentals
    "status": "success"
  }
  ```

#### `GET /health`
- **Description**: System health check
- **Response**:
  ```json
  {
    "status": "healthy"
  }
  ```

## 🔬 Model Details

### Linear Regression Equation
```
cnt = 0.3535 + 0.228*yr + 0.526*temp - 0.189*hum - 0.165*windspeed 
      - 0.113*Spring + 0.045*Winter - 0.59*Aug - 0.124*Jul 
      - 0.05*Jun - 0.045*Light_rainfall - 0.203*Thunderstrom
```

### Key Insights
- **Temperature Impact**: Strong positive correlation (coefficient: 0.526)
- **Year Growth**: Significant growth year-over-year (coefficient: 0.228)
- **Weather Sensitivity**: Storms reduce demand significantly (coefficient: -0.203)
- **Seasonal Patterns**: Summer/Fall show higher activity
- **Model Performance**: R² = 0.834 on test data

### Feature Engineering
- **Categorical Encoding**: One-hot encoding for seasons, months, weather
- **Scaling**: MinMax scaling for numerical features
- **Feature Selection**: RFE (Recursive Feature Elimination)
- **Multicollinearity**: VIF analysis and removal

## 🧪 Testing

### Run All Tests
```bash
python -m pytest test_app.py -v
```

### Test Categories

1. **Unit Tests**: Individual component testing
2. **Integration Tests**: End-to-end workflow testing
3. **API Tests**: HTTP endpoint testing
4. **Model Tests**: Prediction accuracy validation
5. **Edge Case Tests**: Boundary value testing

### Test Coverage
- ✅ Predictor class initialization
- ✅ Input preprocessing
- ✅ Prediction functionality
- ✅ Flask app endpoints
- ✅ Error handling
- ✅ Edge cases and boundary values
- ✅ Model consistency
- ✅ Integration workflows

## 🛠 Technologies Used

### Backend
- **Flask 2.3.3**: Web framework
- **Pandas 1.5.3**: Data manipulation
- **NumPy 1.24.4**: Numerical computing
- **Scikit-learn 1.3.0**: Machine learning
- **Statsmodels 0.14.0**: Statistical analysis

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript**: Interactive functionality
- **Font Awesome**: Icons and UI elements

### Testing & Development
- **Pytest 7.4.2**: Testing framework
- **Pytest-Flask**: Flask-specific testing utilities

### Visualization (Original Analysis)
- **Matplotlib 3.7.2**: Plotting
- **Seaborn 0.12.2**: Statistical visualization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests with coverage
pytest --cov=app test_app.py

# Format code
black app.py test_app.py

# Lint code
flake8 app.py test_app.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Acknowledgments

- Original analysis by [@itsshaliniS](https://github.com/itsshaliniS)
- Dataset from BoomBikes bike-sharing system
- Community contributions and feedback

## 📞 Contact

- **Project Maintainer**: Data Science Team
- **Email**: team@example.com
- **GitHub**: [@vannu07](https://github.com/vannu07)

---

⭐ **Star this repository if you found it helpful!**