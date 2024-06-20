import unittest
from unittest.mock import patch, Mock, call
from flask import Flask, request, jsonify, redirect, url_for, render_template
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from backend.registration import app, connect_db, init_db, reset_db, register, login, logout


class TestRegistration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.db_name = 'test_users.db'
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{self.db_name}'
        init_db()

    def tearDown(self):
        reset_db()

    @patch('registration.connect_db')
    def test_register_new_user(self, mock_connect_db):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None
        mock_conn = Mock()
        mock_conn.__enter__.return_value = mock_cursor
        mock_connect_db.return_value = mock_conn

        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'country_of_residence': 'USA',
            'email': 'john@example.com',
            'password': 'password'
        }

        response = self.app.post('/register', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)

        mock_cursor.execute.assert_has_calls([
            call('SELECT * FROM users WHERE email = ?', ('john@example.com',)),
            call('INSERT INTO users (first_name, last_name, date_of_birth, country_of_residence, email, password) VALUES (?, ?, ?, ?, ?, ?)', ('John', 'Doe', '1980-01-01', 'USA', 'john@example.com', 'password'))
        ])
        mock_conn.commit.assert_called_once()

    @patch('registration.connect_db')
    def test_register_existing_user(self, mock_connect_db):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = {'id': 1}
        mock_conn = Mock()
        mock_conn.__enter__.return_value = mock_cursor
        mock_connect_db.return_value = mock_conn

        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'country_of_residence': 'USA',
            'email': 'john@example.com',
            'password': 'password'
        }

        response = self.app.post('/register', data=data, follow_redirects=False)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Email already registered', response.data)

        mock_cursor.execute.assert_called_once_with('SELECT * FROM users WHERE email = ?', ('john@example.com',))

    @patch('registration.connect_db')
    @patch('registration.login_user')
    def test_login_valid_user(self, mock_login_user, mock_connect_db):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = {'id': 1, 'password': 'password'}
        mock_conn = Mock()
        mock_conn.__enter__.return_value = mock_cursor
        mock_connect_db.return_value = mock_conn

        data = {
            'email': 'john@example.com',
            'password': 'password'
        }

        response = self.app.post('/login', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Flight Search', response.data)

        mock_cursor.execute.assert_called_once_with('SELECT * FROM users WHERE email = ?', ('john@example.com',))
        mock_login_user.assert_called_once_with(Mock())

    @patch('registration.connect_db')
    @patch('registration.logout_user')
    def test_logout(self, mock_logout_user, mock_connect_db):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home', response.data)

        mock_logout_user.assert_called_once()

if __name__ == '__main__':
    unittest.main()
