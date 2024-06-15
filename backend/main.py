from flask import Flask, request, jsonify
from registration import register_user, connect_db, init_db
from flight_search import search_flights
from activities_search import search_activities

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    return register_user()

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    origin = data.get('origin')
    budget = data.get('budget')
    departure_date = data.get('departure_date')
    return_date = data.get('return_date')

    flights = search_flights(origin, budget, departure_date, return_date)

    results = []
    for flight in flights['data']:
        destination = flight['itineraries'][0]['segments'][0]['arrival']['iataCode']
        activities = search_activities(city_name=destination, radius=10)
        results.append({
            'flight': flight,
            'activities': activities
        })

    return jsonify(results)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
