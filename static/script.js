document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const resultContainer = document.getElementById('resultContainer');
    const predictionValue = document.getElementById('predictionValue');
    const predictBtn = document.querySelector('.predict-btn');

    // Auto-populate season based on month selection
    const monthSelect = document.getElementById('month');
    const seasonSelect = document.getElementById('season');

    monthSelect.addEventListener('change', function() {
        const month = this.value;
        const seasonMap = {
            'Dec': 'Winter', 'Jan': 'Winter', 'Feb': 'Winter',
            'Mar': 'Spring', 'Apr': 'Spring', 'May': 'Spring',
            'Jun': 'Summer', 'Jul': 'Summer', 'Aug': 'Summer',
            'Sep': 'Fall', 'Oct': 'Fall', 'Nov': 'Fall'
        };
        
        if (seasonMap[month]) {
            seasonSelect.value = seasonMap[month];
        }
    });

    // Form validation
    function validateForm() {
        const requiredFields = ['year', 'month', 'weekday', 'temperature', 'humidity', 'windspeed', 'weather', 'season'];
        let isValid = true;
        
        requiredFields.forEach(field => {
            const element = document.getElementById(field);
            if (!element.value) {
                element.style.borderColor = '#dc3545';
                isValid = false;
            } else {
                element.style.borderColor = '#e0e0e0';
            }
        });
        
        return isValid;
    }

    // Show loading state
    function showLoading() {
        predictBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Predicting...';
        predictBtn.disabled = true;
        resultContainer.style.display = 'none';
    }

    // Hide loading state
    function hideLoading() {
        predictBtn.innerHTML = '<i class="fas fa-chart-line"></i> Predict Bike Demand';
        predictBtn.disabled = false;
    }

    // Show result with animation
    function showResult(prediction) {
        resultContainer.style.display = 'block';
        
        // Animate the prediction value
        let currentValue = 0;
        const targetValue = prediction;
        const increment = targetValue / 50;
        
        const animateValue = () => {
            if (currentValue < targetValue) {
                currentValue += increment;
                predictionValue.textContent = Math.round(currentValue);
                requestAnimationFrame(animateValue);
            } else {
                predictionValue.textContent = targetValue;
            }
        };
        
        animateValue();
        
        // Scroll to result
        resultContainer.scrollIntoView({ behavior: 'smooth' });
    }

    // Show error message
    function showError(message) {
        hideLoading();
        
        // Remove existing error/success messages
        const existingError = document.querySelector('.error-message');
        const existingSuccess = document.querySelector('.success-message');
        
        if (existingError) existingError.remove();
        if (existingSuccess) existingSuccess.remove();
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.display = 'block';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;
        
        form.appendChild(errorDiv);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }

    // Show success message
    function showSuccess(message) {
        const existingError = document.querySelector('.error-message');
        const existingSuccess = document.querySelector('.success-message');
        
        if (existingError) existingError.remove();
        if (existingSuccess) existingSuccess.remove();
        
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.style.display = 'block';
        successDiv.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
        
        form.appendChild(successDiv);
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            successDiv.remove();
        }, 3000);
    }

    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!validateForm()) {
            showError('Please fill in all required fields');
            return;
        }
        
        showLoading();
        
        try {
            const formData = new FormData(form);
            const data = {
                year: parseInt(formData.get('year')),
                month: formData.get('month'),
                weekday: formData.get('weekday'),
                temperature: parseFloat(formData.get('temperature')),
                humidity: parseFloat(formData.get('humidity')),
                windspeed: parseFloat(formData.get('windspeed')),
                weather: formData.get('weather'),
                season: formData.get('season'),
                holiday: parseInt(formData.get('holiday')),
                workingday: parseInt(formData.get('workingday'))
            };
            
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                hideLoading();
                showResult(result.prediction);
                showSuccess('Prediction completed successfully!');
            } else {
                showError(result.error || 'An error occurred while making the prediction');
            }
            
        } catch (error) {
            console.error('Error:', error);
            showError('Network error. Please check your connection and try again.');
        }
    });

    // Input validation for numeric fields
    const numericInputs = ['temperature', 'humidity', 'windspeed'];
    
    numericInputs.forEach(fieldId => {
        const input = document.getElementById(fieldId);
        
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            const min = parseFloat(this.min);
            const max = parseFloat(this.max);
            
            if (value < min || value > max) {
                this.style.borderColor = '#dc3545';
            } else {
                this.style.borderColor = '#e0e0e0';
            }
        });
    });

    // Add sample data button for testing
    const sampleDataBtn = document.createElement('button');
    sampleDataBtn.type = 'button';
    sampleDataBtn.className = 'sample-data-btn';
    sampleDataBtn.innerHTML = '<i class="fas fa-flask"></i> Load Sample Data';
    sampleDataBtn.style.cssText = `
        width: 100%;
        padding: 10px 20px;
        background: #28a745;
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 0.9rem;
        cursor: pointer;
        margin-top: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        transition: all 0.3s ease;
    `;
    
    sampleDataBtn.addEventListener('click', function() {
        // Fill form with sample data
        document.getElementById('year').value = '1';
        document.getElementById('month').value = 'Jul';
        document.getElementById('weekday').value = 'Mon';
        document.getElementById('temperature').value = '25.5';
        document.getElementById('humidity').value = '65';
        document.getElementById('windspeed').value = '12.5';
        document.getElementById('weather').value = 'Clear';
        document.getElementById('season').value = 'Summer';
        document.getElementById('holiday').value = '0';
        document.getElementById('workingday').value = '1';
        
        showSuccess('Sample data loaded! Click "Predict Bike Demand" to see the result.');
    });
    
    form.appendChild(sampleDataBtn);

    // Add hover effects
    sampleDataBtn.addEventListener('mouseenter', function() {
        this.style.background = '#218838';
        this.style.transform = 'translateY(-2px)';
    });
    
    sampleDataBtn.addEventListener('mouseleave', function() {
        this.style.background = '#28a745';
        this.style.transform = 'translateY(0)';
    });
});
