import unittest
from unittest.mock import patch, Mock
import sys
import os

# Add the backend directory to the system path
# to allow importing the activities_search module
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
)
from backend.activities_search import search_activities, display_top_activities


class TestActivitiesSearch(unittest.TestCase):
    # Test the search_activities function with a city name
    @patch("activities_search.requests.get")
    @patch("activities_search.get_coordinates")
    def test_search_activities_with_city_name(
        self, mock_get_coordinates, mock_requests_get
    ):
        mock_get_coordinates.return_value = (
            41.3850639,
            2.1734035,
        )  # Set up mock coordinates for Barcelona
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [
                {
                    "name": "Tour de la Sagrada Familia",
                    "shortDescription": "Visite de la Sagrada Familia",
                    "price": "€35",
                    "duration": "1.5 heures",
                    "location": {
                        "address": "Carrer de Mallorca, 401, 08013 Barcelona, Espagne"
                    },
                }
            ]
        }
        # Set up a mock response with sample data
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        result = search_activities(city_name="Barcelona", radius=1)
        self.assertEqual(result, mock_response.json.return_value)

    def test_display_top_activities(self, mock_search_activities):
        mock_search_activities.return_value = {
            "data": [
                {
                    "name": "Tour de la Sagrada Familia",
                    "shortDescription": "Visite de la Sagrada Familia",
                    "price": "€35",
                    "duration": "1.5 heures",
                    "location": {
                        "address": "Carrer de Mallorca, 401, 08013 Barcelona, Espagne"
                    },
                },
                {
                    "name": "Balade à vélo dans Barcelone",
                    "shortDescription": "Découvrez Barcelone à vélo",
                    "price": "€25",
                    "duration": "2 heures",
                    "location": {
                        "address": "Plaça de Catalunya, 08002 Barcelona, Espagne"
                    },
                },
            ]
        }

        with patch("builtins.print") as mock_print:
            display_top_activities(city_name="Barcelona", radius=1)
            mock_print.assert_called_with("Activité 1: Tour de la Sagrada Familia")
            mock_print.assert_called_with(
                "    Description: Visite de la Sagrada Familia"
            )
            mock_print.assert_called_with("    Prix: €35")
            mock_print.assert_called_with("    Durée: 1.5 heures")
            mock_print.assert_called_with(
                "    Lieu: Carrer de Mallorca, 401, 08013 Barcelona, Espagne"
            )


if __name__ == "__main__":
    unittest.main()
