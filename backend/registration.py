from flask import Flask, request, jsonify, redirect, url_for, render_template
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flight_search import search_flights
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def connect_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect_db() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            country_of_residence TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        conn.commit()

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        date_of_birth = data.get('date_of_birth')
        country_of_residence = data.get('country_of_residence')
        email = data.get('email')
        password = data.get('password')

        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                return jsonify({"status": "error", "message": "Email already registered"}), 400

            cursor.execute('''
                INSERT INTO users (first_name, last_name, date_of_birth, country_of_residence, email, password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (first_name, last_name, date_of_birth, country_of_residence, email, password))
            conn.commit()

            return redirect(url_for('register_success'))

    return render_template('register.html')

@app.route('/register_success')
def register_success():
    return render_template('register_success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()

            if user and user['password'] == password:
                user_obj = User(user['id'])
                login_user(user_obj)
                return redirect(url_for('flight_search'))
            else:
                return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    return render_template('login.html')

@app.route('/flight_search')
@login_required
def flight_search():
    return render_template('flight_search.html', user=current_user)

@app.route('/flight_search_results', methods=['POST'])
@login_required
def flight_search_results():
    if request.method == 'POST':
        origin = request.form.get('origin')
        budget = request.form.get('budget')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date')

        try:
            flights = search_flights(origin, budget, departure_date, return_date)
            return render_template('flight_search_results.html', flights=flights)
        except requests.exceptions.HTTPError as err:
            return f"HTTP error occurred: {err}"
        except Exception as err:
            return f"An error occurred: {err}"

    return redirect(url_for('flight_search'))  # Redirection vers la page de recherche si aucune donnée n'est reçue


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
