import unittest
from unittest.mock import patch, Mock
import requests
import sys
import os

# Adjust the system path to include the backend directory
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
)

# Import the functions to be tested
from flight_search import search_flight_destinations, extract_flight_information, find_unique_destinations  # type: ignore


class TestFlightSearchFunctions(unittest.TestCase):
    def setUp(self):
        # Setup initial test data
        self.origin = "PAR"
        self.departure_date = "2024-07-30"
        self.one_way = False
        self.non_stop = False
        self.max_price = 300

    @patch("flight_search.create_auth_headers")
    @patch("requests.get")
    def test_search_flight_destinations_success(
        self, mock_get, mock_create_auth_headers
    ):
        # Mock a successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [
                {
                    "destination": "LON",
                    "departureDate": "2024-07-30",
                    "price": {"total": "200"},
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        mock_create_auth_headers.return_value = {"Authorization": "Bearer abc123"}

        # Call the function and assert the results
        result = search_flight_destinations(
            self.origin,
            self.departure_date,
            self.one_way,
            self.non_stop,
            self.max_price,
        )
        self.assertIsNotNone(result)
        self.assertIn("data", result)

    @patch("flight_search.create_auth_headers")
    @patch("requests.get")
    def test_search_flight_destinations_http_error(
        self, mock_get, mock_create_auth_headers
    ):
        # Mock an API response with HTTP error
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "HTTP Error"
        )
        mock_response.content = b'{"error": "API Error"}'
        mock_get.return_value = mock_response
        mock_create_auth_headers.return_value = {"Authorization": "Bearer abc123"}

        # Call the function and assert the result is None due to error
        result = search_flight_destinations(
            self.origin,
            self.departure_date,
            self.one_way,
            self.non_stop,
            self.max_price,
        )
        self.assertIsNone(result)

    def test_extract_flight_information_success(self):
        # Test extracting information from a valid flight offer
        flight_offer = {
            "destination": {"iataCode": "LON", "name": "London"},
            "departureDate": "2024-07-30",
            "returnDate": "2024-08-06",
            "price": {"total": "200"},
        }

        result = extract_flight_information(flight_offer)
        self.assertIsNotNone(result)
        self.assertEqual(result["destination"]["iataCode"], "LON")
        self.assertEqual(result["departure_date"], "2024-07-30")
        self.assertEqual(result["return_date"], "2024-08-06")
        self.assertEqual(result["price_total"], "200")

    def test_extract_flight_information_missing_data(self):
        # Test extracting information from an invalid flight offer
        flight_offer = {}
        result = extract_flight_information(flight_offer)
        self.assertIsNone(result)

    @patch("flight_search.search_flight_destinations")
    @patch("flight_search.extract_flight_information")
    def test_find_unique_destinations_success(
        self, mock_extract_flight_information, mock_search_flight_destinations
    ):
        # Mock the search and extraction functions for successful unique destination search
        mock_search_flight_destinations.return_value = {
            "data": [
                {"destination": {"iataCode": "LON", "name": "London"}},
                {"destination": {"iataCode": "NYC", "name": "New York"}},
            ]
        }

        mock_extract_flight_information.side_effect = [
            {
                "destination": "LON",
                "departure_date": "2024-07-30",
                "return_date": "2024-08-06",
                "price_total": "200",
            },
            {
                "destination": "NYC",
                "departure_date": "2024-07-30",
                "return_date": "2024-08-06",
                "price_total": "400",
            },
        ]

        result = find_unique_destinations(
            self.origin,
            self.departure_date,
            self.one_way,
            self.non_stop,
            self.max_price,
        )
        self.assertEqual(len(result), 2)

    @patch("flight_search.search_flight_destinations")
    def test_find_unique_destinations_no_data(self, mock_search_flight_destinations):
        # Mock the search function to return no data
        mock_search_flight_destinations.return_value = {}
        result = find_unique_destinations(
            self.origin,
            self.departure_date,
            self.one_way,
            self.non_stop,
            self.max_price,
        )
        self.assertEqual(result, [])


if __name__ == "__main__":
    # Run the tests
    unittest.main()
