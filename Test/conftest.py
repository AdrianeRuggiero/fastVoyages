import sys
import os
import pytest

# Calculer le chemin absolu du répertoire 'fastVoyages'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Ajouter le répertoire 'fastVoyages' au sys.path
sys.path.insert(0, project_root)

# Si 'flight_search.py' est dans un répertoire différent, ajoutez également ce répertoire
sys.path.insert(0, os.path.join(project_root, 'backend'))

print("sys.path:", sys.path)  # Debug: Print sys.path to check if the path is correctly added

from backend.registration import app, init_db, connect_db

@pytest.fixture
def client():
    # Configure Flask application for testing
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        # Recreate the database schema for testing
        init_db()
        yield app.test_client()
        # Drop all data after the test
        with connect_db() as conn:
            conn.execute('DROP TABLE IF EXISTS users')
            conn.commit()

@pytest.fixture
def mock_requests():
    import requests_mock
    with requests_mock.Mocker() as m:
        yield m