import unittest
from unittest.mock import patch, Mock, call
from dotenv import load_dotenv
import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
)


from backend.auth_amadeus import get_access_token, create_auth_headers


class TestAuthAmadeus(unittest.TestCase):
    @patch("auth_amadeus.os.getenv")
    @patch("auth_amadeus.requests.post")
    def test_get_access_token(self, mock_requests_post, mock_getenv):
        mock_getenv.side_effect = ["mock_client_id", "mock_client_secret"]
        mock_response = Mock()
        mock_response.json.return_value = {"access_token": "mock_access_token"}
        mock_requests_post.return_value = mock_response

        access_token = get_access_token()

        mock_getenv.assert_has_calls([call("CLIENT_ID"), call("CLIENT_SECRET")])
        mock_requests_post.assert_called_with(
            "https://test.api.amadeus.com/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": "mock_client_id",
                "client_secret": "mock_client_secret",
            },
        )
        self.assertEqual(access_token, "mock_access_token")

    @patch("auth_amadeus.get_access_token")
    def test_create_auth_headers(self, mock_get_access_token):
        mock_get_access_token.return_value = "mock_access_token"

        auth_headers = create_auth_headers()

        mock_get_access_token.assert_called_once()
        self.assertEqual(auth_headers, {"Authorization": "Bearer mock_access_token"})


if __name__ == "__main__":
    unittest.main()
