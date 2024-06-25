import requests
from auth_amadeus import create_auth_headers


def search_flight_destinations(origin, departure_date, one_way, non_stop, max_price):
    """
    Search for flight destinations based on provided criteria.

    Args:
        origin (str): IATA code for the origin city.
        departure_date (str): Departure date in the format YYYY-MM-DD.
        one_way (bool): Indicates if the flight is one way.
        non_stop (bool): Indicates if the flight should be non-stop.
        max_price (int): Maximum budget for the flight in USD.

    Returns:
        dict: JSON response from the Amadeus API containing flight destinations.
    """
    try:
        url = 'https://test.api.amadeus.com/v1/shopping/flight-destinations'

        params = {
            'origin': origin,
            'departureDate': departure_date,
            'oneWay': one_way,
            'nonStop': non_stop,
            'maxPrice': max_price
        }

        headers = create_auth_headers()

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as http_err:
        # Print HTTP error details
        print(f"HTTP Error: {http_err}")
        print(f"API Response: {response.content}")
        return None
    except requests.exceptions.RequestException as req_err:
        # Print request error details
        print(f"Request Error: {req_err}")
        return None
    except Exception as ex:
        # Print unexpected error details
        print(f"Unexpected Error: {ex}")
        return None


def extract_flight_information(flight_offer):
    """
    Extract relevant flight information from the flight offer.

    Args:
        flight_offer (dict): Flight offer containing details of a flight.

    Returns:
        dict: Extracted flight information.
    """
    try:
        destination_info = flight_offer.get('destination')
        departure_date = flight_offer.get('departureDate')
        return_date = flight_offer.get('returnDate', None)
        price_total = flight_offer.get('price', {}).get('total', 'N/A')
        links = flight_offer.get('links', {})

        return {
            'destination': destination_info,
            'departure_date': departure_date,
            'return_date': return_date,
            'price_total': price_total,
            'flight_dates_link': links.get('flightDates', 'N/A'),
            'flight_offers_link': links.get('flightOffers', 'N/A')
        }
    except Exception as ex:
        # Print error details if extraction fails
        print(f"Error extracting flight information: {ex}")
        return None


def find_unique_destinations(origin, departure_date, one_way, non_stop, max_price, num_destinations=5):
    """
    Find unique flight destinations based on provided criteria.

    Args:
        origin (str): IATA code for the origin city.
        departure_date (str): Departure date in the format YYYY-MM-DD.
        one_way (bool): Indicates if the flight is one way.
        non_stop (bool): Indicates if the flight should be non-stop.
        max_price (int): Maximum budget for the flight in USD.
        num_destinations (int, optional): Number of unique destinations to find. Defaults to 5.

    Returns:
        list: A list of dictionaries containing flight information for unique destinations.
    """
    try:
        # Get available flight offers
        destinations = search_flight_destinations(origin, departure_date, one_way, non_stop, max_price)
        if not destinations or 'data' not in destinations:
            print("No destinations found.")
            return []

        flight_offers = destinations['data']

        unique_destinations = []
        seen_destinations = set()

        for offer in flight_offers:
            destination_info = offer.get('destination')
            if destination_info not in seen_destinations and len(unique_destinations) < num_destinations:
                seen_destinations.add(destination_info)
                flight_info = extract_flight_information(offer)
                if flight_info:
                    unique_destinations.append(flight_info)

        return unique_destinations

    except Exception as ex:
        # Print error details if any error occurs
        print(f"Error: {ex}")
        return []


# Example usage
if __name__ == "__main__":
    origin = 'PAR'  # IATA code for Paris
    departure_date = '2024-07-30'  # Departure date (format YYYY-MM-DD)
    one_way = False  # Round-trip flights
    non_stop = False  # Flights with stops
    max_price = 300  # Maximum budget in USD

    num_destinations = 5  # Number of unique destinations to find

    # Find and display the top 5 unique destinations
    unique_destinations = find_unique_destinations(
        origin, departure_date, one_way, non_stop, max_price, num_destinations
    )
    if unique_destinations:
        print("Information on the top 5 unique destinations:")
        for idx, destination in enumerate(unique_destinations, start=1):
            print(f"{idx}. Destination: {destination['destination']}")
            print(f"   Departure Date: {destination['departure_date']}")
            if destination['return_date']:
                print(f"   Return Date: {destination['return_date']}")
            print(f"   Total Price: {destination['price_total']}")
            print("   Links to flight details:")
            print(f"   - Flight Dates: {destination['flight_dates_link']}")
            print(f"   - Flight Offers: {destination['flight_offers_link']}")
            print("\n")
    else:
        print("No unique destinations found.")
