from flask import Flask, request, render_template, redirect, url_for
from flight_search import search_flights  # Importez la fonction search_flights depuis flight_search.py
import requests

app = Flask(__name__)

# Autres routes et configuration...

@app.route('/flight_search_results', methods=['POST'])
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

    return redirect(url_for('flight_search'))  # Redirigez l'utilisateur vers la page de recherche si aucune donnée n'est reçue

# Autres routes et configuration...

if __name__ == '__main__':
    app.run(debug=True)
