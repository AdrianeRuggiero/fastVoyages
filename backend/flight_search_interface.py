from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from registration import connect_db  # Importez la fonction connect_db de registration.py
from flight_search import search_flights

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Remplacez par votre clé secrète

# Initialisation de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Fonction pour charger l'utilisateur depuis la base de données (à adapter)
@login_manager.user_loader
def load_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(user['id'], user['username'], user['email'])  # Adapter selon votre structure d'utilisateur

# Page d'accueil après la connexion
@app.route('/')
@login_required
def home():
    return render_template('home.html', username=current_user.username)  # Adapter selon vos besoins

# Formulaire de recherche de vols
@app.route('/search_flights', methods=['GET', 'POST'])
@login_required
def search_flights_page():
    if request.method == 'POST':
        origin = request.form['origin']
        budget = float(request.form['budget'])  # Assurez-vous que le budget est converti en float si nécessaire
        departure_date = request.form['departure_date']
        return_date = request.form['return_date']
        
        try:
            flights = search_flights(origin, budget, departure_date, return_date)
            return render_template('flights_result.html', flights=flights)
        except Exception as e:
            return render_template('error.html', error=str(e))
    
    return render_template('flight_search_form.html')

if __name__ == '__main__':
    app.run(debug=True)
