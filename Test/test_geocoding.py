import unittest
from unittest.mock import patch, Mock
import os
from dotenv import load_dotenv
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from geocoding import get_coordinates

class TestGeocoding(unittest.TestCase):
    @patch('geocoding.os.getenv')
    @patch('geocoding.OpenCageGeocode')
    def test_get_coordinates(self, mock_opencage_geocode, mock_getenv):
        mock_getenv.return_value = 'mock_api_key'

        mock_geocoder = Mock()
        mock_geocoder.geocode.return_value = [
            {
                'geometry': {
                    'lat': 48.8566,
                    'lng': 2.3522
                }
            }
        ]
        mock_opencage_geocode.return_value = mock_geocoder

        latitude, longitude = get_coordinates('Paris')

        mock_getenv.assert_called_with('OPENCAGE_API_KEY')
        mock_opencage_geocode.assert_called_with('mock_api_key')
        mock_geocoder.geocode.assert_called_with('Paris')
        self.assertEqual(latitude, 48.8566)
        self.assertEqual(longitude, 2.3522)

    @patch('geocoding.os.getenv')
    @patch('geocoding.OpenCageGeocode')
    def test_get_coordinates_no_results(self, mock_opencage_geocode, mock_getenv):
        mock_getenv.return_value = 'mock_api_key'

        mock_geocoder = Mock()
        mock_geocoder.geocode.return_value = []
        mock_opencage_geocode.return_value = mock_geocoder

        with self.assertRaises(ValueError):
            get_coordinates('NonExistentCity')

        mock_getenv.assert_called_with('OPENCAGE_API_KEY')
        mock_opencage_geocode.assert_called_with('mock_api_key')
        mock_geocoder.geocode.assert_called_with('NonExistentCity')

if __name__ == '__main__':
    unittest.main()
