import unittest
from unittest.mock import patch, Mock, call
from dotenv import load_dotenv
import sys
import os

# Adjust the system path to include the backend directory
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
)

# Import the functions to be tested
from backend.auth_amadeus import get_access_token, create_auth_headers


class TestAuthAmadeus(unittest.TestCase):
    @patch("auth_amadeus.os.getenv")
    @patch("auth_amadeus.requests.post")
    def test_get_access_token(self, mock_requests_post, mock_getenv):
        # Mock the environment variables for client ID and client secret
        mock_getenv.side_effect = ["mock_client_id", "mock_client_secret"]
        # Mock the response from the token request
        mock_response = Mock()
        mock_response.json.return_value = {"access_token": "mock_access_token"}
        mock_requests_post.return_value = mock_response

        # Call the function to get the access token
        access_token = get_access_token()

        # Assert the environment variables were accessed correctly
        mock_getenv.assert_has_calls([call("CLIENT_ID"), call("CLIENT_SECRET")])
        # Assert the request was made with correct parameters
        mock_requests_post.assert_called_with(
            "https://test.api.amadeus.com/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": "mock_client_id",
                "client_secret": "mock_client_secret",
            },
        )
        # Assert the access token is as expected
        self.assertEqual(access_token, "mock_access_token")

    @patch("auth_amadeus.get_access_token")
    def test_create_auth_headers(self, mock_get_access_token):
        # Mock the access token retrieval function
        mock_get_access_token.return_value = "mock_access_token"

        # Call the function to create authentication headers
        auth_headers = create_auth_headers()

        # Assert the get_access_token function was called once
        mock_get_access_token.assert_called_once()
        # Assert the headers are as expected
        self.assertEqual(auth_headers, {"Authorization": "Bearer mock_access_token"})


if __name__ == "__main__":
    # Run the tests
    unittest.main()
