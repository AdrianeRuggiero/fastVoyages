# tests/test_registration.py
import json

def test_register_and_login(client):
    # Test user registration
    response = client.post('/register', data={
        'first_name': 'John',
        'last_name': 'Doe',
        'date_of_birth': '1990-01-01',
        'country_of_residence': 'France',
        'email': 'john.doe@example.com',
        'password': 'password123'
    })
    assert response.status_code == 302  # Redirection after successful registration

    # Test login
    response = client.post('/login', data={
        'email': 'john.doe@example.com',
        'password': 'password123'
    })
    assert response.status_code == 302  # Redirection after successful login