import unittest
from unittest.mock import patch, Mock
import os
from dotenv import load_dotenv
import sys

# Adjust the system path to include the backend directory
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
)

# Import the function to be tested
from geocoding import get_coordinates


class TestGeocoding(unittest.TestCase):
    @patch("geocoding.os.getenv")
    @patch("geocoding.OpenCageGeocode")
    def test_get_coordinates(self, mock_opencage_geocode, mock_getenv):
        # Mock the environment variable for the API key
        mock_getenv.return_value = "mock_api_key"

        # Mock the geocoder object and its response
        mock_geocoder = Mock()
        mock_geocoder.geocode.return_value = [
            {"geometry": {"lat": 48.8566, "lng": 2.3522}}
        ]
        mock_opencage_geocode.return_value = mock_geocoder

        # Call the function to get the coordinates
        latitude, longitude = get_coordinates("Paris")

        # Assert the environment variable was accessed correctly
        mock_getenv.assert_called_with("OPENCAGE_API_KEY")
        # Assert the OpenCageGeocode object was created with the correct API key
        mock_opencage_geocode.assert_called_with("mock_api_key")
        # Assert the geocode method was called with the correct city
        mock_geocoder.geocode.assert_called_with("Paris")
        # Assert the returned coordinates are as expected
        self.assertEqual(latitude, 48.8566)
        self.assertEqual(longitude, 2.3522)

    @patch("geocoding.os.getenv")
    @patch("geocoding.OpenCageGeocode")
    def test_get_coordinates_no_results(self, mock_opencage_geocode, mock_getenv):
        # Mock the environment variable for the API key
        mock_getenv.return_value = "mock_api_key"

        # Mock the geocoder object and its response with no results
        mock_geocoder = Mock()
        mock_geocoder.geocode.return_value = []
        mock_opencage_geocode.return_value = mock_geocoder

        # Call the function to get the coordinates and assert it raises a ValueError
        with self.assertRaises(ValueError):
            get_coordinates("NonExistentCity")

        # Assert the environment variable was accessed correctly
        mock_getenv.assert_called_with("OPENCAGE_API_KEY")
        # Assert the OpenCageGeocode object was created with the correct API key
        mock_opencage_geocode.assert_called_with("mock_api_key")
        # Assert the geocode method was called with the correct city
        mock_geocoder.geocode.assert_called_with("NonExistentCity")


if __name__ == "__main__":
    # Run the tests
    unittest.main()
