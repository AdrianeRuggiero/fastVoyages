import pytest

def test_search_activities(client, mock_requests, mocker):
    # Mock the OpenCage API response
    mock_requests.get('https://api.opencagedata.com/geocode/v1/json', json={
        'results': [{'geometry': {'lat': 41.3851, 'lng': 2.1734}}]
    })
    
    # Mock the Amadeus API response
    mock_requests.get('https://test.api.amadeus.com/v1/shopping/activities', json={
        'data': [
            {
                'name': 'Sagrada Familia',
                'shortDescription': 'A famous church in Barcelona',
                'price': '20 EUR',
                'duration': '2 hours',
                'location': {'address': 'Carrer de Mallorca, 401, 08013 Barcelona, Spain'}
            }
        ]
    })

    response = client.get('/activities_search?city_name=Barcelone&radius=1')
    assert response.status_code == 200
    assert b'Sagrada Familia' in response.data
