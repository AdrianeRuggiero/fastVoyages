from flask import Flask, render_template, request
from flask_login import LoginManager, login_required, current_user
from registration import connect_db  # Import the function connect_db from registration.py
from flight_search import find_unique_destinations

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with your secret key

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Function to load the user from the database (adapt as necessary)
@login_manager.user_loader
def load_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(user['id'])  # Adjust according to your user structure

@app.route('/')
@login_required
def home():
    return render_template('home.html', username=current_user.id)  # Adjust as needed

# Flight search form
@app.route('/search_flights', methods=['GET', 'POST'])
@login_required
def search_flights_page():
    if request.method == 'POST':
        origin = request.form['origin']
        budget = float(request.form['budget'])  # Ensure budget is converted to float if necessary
        departure_date = request.form['departure_date']
        return_date = request.form['return_date']
        one_way = request.form.get('one_way') == 'on'
        non_stop = request.form.get('non_stop') == 'on'

        try:
            flights = find_unique_destinations(origin, departure_date, one_way, non_stop, budget, num_destinations=5)
            return render_template('flights_result.html', flights=flights)
        except Exception as e:
            return render_template('error.html', error=str(e))
    
    return render_template('flight_search_form.html')

if __name__ == '__main__':
    app.run(debug=True)
