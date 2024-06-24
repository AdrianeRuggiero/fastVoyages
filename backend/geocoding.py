import os
from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode

# Load environment variables from the .env file
load_dotenv()


def get_coordinates(city_name):
    """
    Get the geographical coordinates (latitude and longitude) for a given city.

    Args:
        city_name (str): The name of the city for which to find coordinates.

    Returns:
        tuple: A tuple containing the latitude and longitude of the city.

    Raises:
        ValueError: If the city name cannot be found.
    """
    # Retrieve the OpenCage API key from environment variables
    api_key = os.getenv('OPENCAGE_API_KEY')
    geocoder = OpenCageGeocode(api_key)

    # Perform the geocoding request
    results = geocoder.geocode(city_name)

    # Check if results were returned and extract coordinates
    if results and len(results) > 0:
        latitude = results[0]['geometry']['lat']
        longitude = results[0]['geometry']['lng']
        return latitude, longitude
    else:
        # Raise an error if no coordinates are found
        raise ValueError(f"Unable to find coordinates for city: {city_name}")


# Example usage
if __name__ == "__main__":
    city_name = "Paris"
    try:
        # Get the coordinates for the specified city
        lat, lng = get_coordinates(city_name)
        print(f"Coordinates of {city_name}: Latitude={lat}, Longitude={lng}")
    except ValueError as e:
        # Print the error message if coordinates cannot be found
        print(e)
