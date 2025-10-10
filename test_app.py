import pytest
import json
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, BikeSharingPredictor

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def predictor():
    """Create a BikeSharingPredictor instance for testing."""
    return BikeSharingPredictor()

class TestBikeSharingPredictor:
    """Test cases for the BikeSharingPredictor class."""
    
    def test_predictor_initialization(self, predictor):
        """Test that the predictor initializes correctly."""
        assert predictor is not None
        assert predictor.coefficients is not None
        assert len(predictor.coefficients) > 0
        assert 'const' in predictor.coefficients
        assert 'temp' in predictor.coefficients
    
    def test_preprocess_input(self, predictor):
        """Test input preprocessing functionality."""
        test_data = {
            'year': 1,
            'temperature': 25.0,
            'humidity': 60.0,
            'windspeed': 10.0,
            'season': 'Summer',
            'month': 'Jul',
            'weather': 'Clear',
            'weekday': 'Mon',
            'holiday': 0,
            'workingday': 1
        }
        
        processed = predictor.preprocess_input(test_data)
        
        assert processed is not None
        assert len(processed.columns) > 0
        assert 'yr' in processed.columns
        assert 'temp' in processed.columns
        assert 'hum' in processed.columns
        assert 'windspeed' in processed.columns
    
    def test_predict_valid_input(self, predictor):
        """Test prediction with valid input data."""
        test_data = {
            'year': 1,
            'temperature': 25.0,
            'humidity': 60.0,
            'windspeed': 10.0,
            'season': 'Summer',
            'month': 'Jul',
            'weather': 'Clear',
            'weekday': 'Mon',
            'holiday': 0,
            'workingday': 1
        }
        
        prediction = predictor.predict(test_data)
        
        assert isinstance(prediction, int)
        assert prediction >= 0
        assert prediction > 0  # Should be a positive prediction
    
    def test_predict_edge_cases(self, predictor):
        """Test prediction with edge case inputs."""
        # Test with minimum values
        min_data = {
            'year': 0,
            'temperature': -10.0,
            'humidity': 0.0,
            'windspeed': 0.0,
            'season': 'Winter',
            'month': 'Jan',
            'weather': 'Thunderstrom',
            'weekday': 'Sun',
            'holiday': 1,
            'workingday': 0
        }
        
        prediction_min = predictor.predict(min_data)
        assert isinstance(prediction_min, int)
        assert prediction_min >= 0
        
        # Test with maximum values
        max_data = {
            'year': 1,
            'temperature': 40.0,
            'humidity': 100.0,
            'windspeed': 50.0,
            'season': 'Summer',
            'month': 'Aug',
            'weather': 'Clear',
            'weekday': 'Fri',
            'holiday': 0,
            'workingday': 1
        }
        
        prediction_max = predictor.predict(max_data)
        assert isinstance(prediction_max, int)
        assert prediction_max >= 0
    
    def test_predict_invalid_input(self, predictor):
        """Test prediction with invalid input data."""
        invalid_data = {
            'year': 'invalid',
            'temperature': 'not_a_number',
            'humidity': None,
            'windspeed': 10.0,
            'season': 'Summer',
            'month': 'Jul',
            'weather': 'Clear',
            'weekday': 'Mon',
            'holiday': 0,
            'workingday': 1
        }
        
        # Should handle invalid input gracefully
        prediction = predictor.predict(invalid_data)
        assert isinstance(prediction, int)
        assert prediction >= 0

class TestFlaskApp:
    """Test cases for the Flask application endpoints."""
    
    def test_index_route(self, client):
        """Test the index route returns the main page."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Bike Sharing Demand Predictor' in response.data
    
    def test_health_route(self, client):
        """Test the health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_predict_valid_data(self, client):
        """Test prediction endpoint with valid data."""
        valid_data = {
            'year': 1,
            'month': 'Jul',
            'weekday': 'Mon',
            'temperature': 25.0,
            'humidity': 60.0,
            'windspeed': 10.0,
            'weather': 'Clear',
            'season': 'Summer',
            'holiday': 0,
            'workingday': 1
        }
        
        response = client.post('/predict', 
                             data=json.dumps(valid_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'prediction' in data
        assert 'status' in data
        assert data['status'] == 'success'
        assert isinstance(data['prediction'], int)
        assert data['prediction'] >= 0
    
    def test_predict_missing_fields(self, client):
        """Test prediction endpoint with missing required fields."""
        incomplete_data = {
            'year': 1,
            'temperature': 25.0,
            # Missing other required fields
        }
        
        response = client.post('/predict',
                             data=json.dumps(incomplete_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Missing required field' in data['error']
    
    def test_predict_invalid_json(self, client):
        """Test prediction endpoint with invalid JSON."""
        response = client.post('/predict',
                             data='invalid json',
                             content_type='application/json')
        
        assert response.status_code == 400
    
    def test_predict_edge_cases(self, client):
        """Test prediction endpoint with edge case values."""
        edge_case_data = {
            'year': 0,
            'month': 'Jan',
            'weekday': 'Sun',
            'temperature': -10.0,
            'humidity': 0.0,
            'windspeed': 0.0,
            'weather': 'Thunderstrom',
            'season': 'Winter',
            'holiday': 1,
            'workingday': 0
        }
        
        response = client.post('/predict',
                             data=json.dumps(edge_case_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert isinstance(data['prediction'], int)
        assert data['prediction'] >= 0
    
    def test_predict_boundary_values(self, client):
        """Test prediction endpoint with boundary values."""
        boundary_data = {
            'year': 1,
            'month': 'Dec',
            'weekday': 'Sat',
            'temperature': 40.0,
            'humidity': 100.0,
            'windspeed': 50.0,
            'weather': 'Clear',
            'season': 'Summer',
            'holiday': 0,
            'workingday': 1
        }
        
        response = client.post('/predict',
                             data=json.dumps(boundary_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert isinstance(data['prediction'], int)
        assert data['prediction'] >= 0

class TestModelAccuracy:
    """Test cases for model accuracy and consistency."""
    
    def test_model_consistency(self, predictor):
        """Test that the model produces consistent results for the same input."""
        test_data = {
            'year': 1,
            'temperature': 25.0,
            'humidity': 60.0,
            'windspeed': 10.0,
            'season': 'Summer',
            'month': 'Jul',
            'weather': 'Clear',
            'weekday': 'Mon',
            'holiday': 0,
            'workingday': 1
        }
        
        prediction1 = predictor.predict(test_data)
        prediction2 = predictor.predict(test_data)
        
        assert prediction1 == prediction2
    
    def test_temperature_impact(self, predictor):
        """Test that temperature has a positive impact on predictions."""
        base_data = {
            'year': 1,
            'temperature': 20.0,
            'humidity': 60.0,
            'windspeed': 10.0,
            'season': 'Summer',
            'month': 'Jul',
            'weather': 'Clear',
            'weekday': 'Mon',
            'holiday': 0,
            'workingday': 1
        }
        
        high_temp_data = base_data.copy()
        high_temp_data['temperature'] = 30.0
        
        prediction_low = predictor.predict(base_data)
        prediction_high = predictor.predict(high_temp_data)
        
        # Higher temperature should generally lead to higher predictions
        assert prediction_high >= prediction_low
    
    def test_weather_impact(self, predictor):
        """Test that weather conditions affect predictions appropriately."""
        base_data = {
            'year': 1,
            'temperature': 25.0,
            'humidity': 60.0,
            'windspeed': 10.0,
            'season': 'Summer',
            'month': 'Jul',
            'weather': 'Clear',
            'weekday': 'Mon',
            'holiday': 0,
            'workingday': 1
        }
        
        clear_prediction = predictor.predict(base_data)
        
        # Test with thunderstorm
        storm_data = base_data.copy()
        storm_data['weather'] = 'Thunderstrom'
        storm_prediction = predictor.predict(storm_data)
        
        # Clear weather should generally have higher predictions than storms
        assert clear_prediction >= storm_prediction

class TestIntegration:
    """Integration tests for the complete system."""
    
    def test_end_to_end_prediction(self, client):
        """Test complete end-to-end prediction workflow."""
        # Test data representing a typical summer day
        test_data = {
            'year': 1,
            'month': 'Jul',
            'weekday': 'Mon',
            'temperature': 28.0,
            'humidity': 55.0,
            'windspeed': 8.0,
            'weather': 'Clear',
            'season': 'Summer',
            'holiday': 0,
            'workingday': 1
        }
        
        # Make prediction request
        response = client.post('/predict',
                             data=json.dumps(test_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert isinstance(data['prediction'], int)
        assert data['prediction'] > 0
        
        # Verify prediction is reasonable (not too high or too low)
        assert 0 <= data['prediction'] <= 10000  # Reasonable range for bike rentals
    
    def test_multiple_predictions(self, client):
        """Test making multiple predictions in sequence."""
        test_cases = [
            {
                'year': 1, 'month': 'Jan', 'weekday': 'Mon',
                'temperature': 5.0, 'humidity': 80.0, 'windspeed': 15.0,
                'weather': 'Light_rainfall', 'season': 'Winter',
                'holiday': 0, 'workingday': 1
            },
            {
                'year': 1, 'month': 'Jul', 'weekday': 'Fri',
                'temperature': 30.0, 'humidity': 50.0, 'windspeed': 5.0,
                'weather': 'Clear', 'season': 'Summer',
                'holiday': 0, 'workingday': 1
            },
            {
                'year': 0, 'month': 'Dec', 'weekday': 'Sun',
                'temperature': -5.0, 'humidity': 90.0, 'windspeed': 20.0,
                'weather': 'Thunderstrom', 'season': 'Winter',
                'holiday': 1, 'workingday': 0
            }
        ]
        
        predictions = []
        for test_data in test_cases:
            response = client.post('/predict',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            predictions.append(data['prediction'])
        
        # All predictions should be valid
        assert len(predictions) == 3
        assert all(isinstance(p, int) for p in predictions)
        assert all(p >= 0 for p in predictions)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
