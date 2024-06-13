from flask import Blueprint, render_template, request, jsonify
from .amadeus_api import search_flights

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    budget = data.get('budget')
    origin = data.get('origin')
    
    if not budget or not origin:
        return jsonify({'error': 'Veuillez fournir un budget et une ville de départ'}), 400
    
    flights = search_flights(origin, budget)
    if 'error' in flights:
        return jsonify(flights), 500
    return jsonify(flights)
