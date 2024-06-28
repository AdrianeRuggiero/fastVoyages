import unittest
from unittest.mock import patch, Mock, call
from flask import Flask, request, jsonify, redirect, url_for, render_template
import sqlite3
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
import sys
import os

# Adjust the system path to include the backend directory
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
)

# Import the functions to be tested from the backend.registration module
from backend.registration import (
    app,
    connect_db,
    init_db,
    reset_db,
    register,
    login,
    logout,
)


class TestRegistration(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client and database configuration for testing
        self.app = app.test_client()
        self.app.testing = True
        self.db_name = "test_users.db"
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{self.db_name}"
        init_db()

    def tearDown(self):
        # Reset the database after each test
        reset_db()

    @patch("registration.connect_db")
    def test_register_new_user(self, mock_connect_db):
        # Mock the database connection and cursor for a new user registration
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None  # No existing user
        mock_conn = Mock()
        mock_conn.__enter__.return_value = mock_cursor
        mock_connect_db.return_value = mock_conn

        # Define the data for a new user registration
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1980-01-01",
            "country_of_residence": "USA",
            "email": "john@example.com",
            "password": "password",
        }

        # Send a POST request to register a new user
        response = self.app.post("/register", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Registration successful", response.data)

        # Assert the correct database queries were executed
        mock_cursor.execute.assert_has_calls(
            [
                call("SELECT * FROM users WHERE email = ?", ("john@example.com",)),
                call(
                    "INSERT INTO users (first_name, last_name, date_of_birth, country_of_residence, email, password) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        "John",
                        "Doe",
                        "1980-01-01",
                        "USA",
                        "john@example.com",
                        "password",
                    ),
                ),
            ]
        )
        # Assert the transaction was committed
        mock_conn.commit.assert_called_once()

    @patch("registration.connect_db")
    def test_register_existing_user(self, mock_connect_db):
        # Mock the database connection and cursor for an existing user registration
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = {"id": 1}  # Existing user
        mock_conn = Mock()
        mock_conn.__enter__.return_value = mock_cursor
        mock_connect_db.return_value = mock_conn

        # Define the data for an existing user registration
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1980-01-01",
            "country_of_residence": "USA",
            "email": "john@example.com",
            "password": "password",
        }

        # Send a POST request to register an existing user
        response = self.app.post("/register", data=data, follow_redirects=False)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Email already registered", response.data)

        # Assert the correct database query was executed
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM users WHERE email = ?", ("john@example.com",)
        )

    @patch("registration.connect_db")
    @patch("registration.login_user")
    def test_login_valid_user(self, mock_login_user, mock_connect_db):
        # Mock the database connection and cursor for a valid user login
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = {"id": 1, "password": "password"}  # Valid user
        mock_conn = Mock()
        mock_conn.__enter__.return_value = mock_cursor
        mock_connect_db.return_value = mock_conn

        # Define the data for a valid user login
        data = {"email": "john@example.com", "password": "password"}

        # Send a POST request to log in the user
        response = self.app.post("/login", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Flight Search", response.data)

        # Assert the correct database query was executed
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM users WHERE email = ?", ("john@example.com",)
        )
        # Assert the login_user function was called
        mock_login_user.assert_called_once_with(Mock())

    @patch("registration.connect_db")
    @patch("registration.logout_user")
    def test_logout(self, mock_logout_user, mock_connect_db):
        # Send a GET request to log out the user
        response = self.app.get("/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Home", response.data)

        # Assert the logout_user function was called
        mock_logout_user.assert_called_once()


if __name__ == "__main__":
    # Run the tests
    unittest.main()
