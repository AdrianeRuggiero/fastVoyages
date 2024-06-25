import requests
from auth_amadeus import create_auth_headers
from geocoding import get_coordinates


def search_activities(latitude=None, longitude=None, radius=1, city_name=None):
    """
    Search for activities based on provided coordinates or city name.

    Args:
        latitude (float, optional): Latitude of the location.
        longitude (float, optional): Longitude of the location.
        radius (int, optional): Search radius in kilometers. Defaults to 1.
        city_name (str, optional): Name of the city. Defaults to None.

    Returns:
        dict: JSON response from the Amadeus API containing activity info.
    """
    try:
        # If city name is provided, get the coordinates from the city name
        if city_name:
            latitude, longitude = get_coordinates(city_name)
        # If neither city name nor coordinates are provided, raise an error
        elif latitude is None or longitude is None:
            raise ValueError("Either city_name or "
                             "both latitude and longitude must be provided")

        # Define the API endpoint and parameters
        url = 'https://test.api.amadeus.com/v1/shopping/activities'
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'radius': radius
        }

        # Create authorization headers
        headers = create_auth_headers()

        # Make a GET request to the Amadeus API
        response = requests.get(url, headers=headers, params=params)

        # Raise an exception for HTTP errors
        response.raise_for_status()

        # Return the JSON response
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        # Print HTTP error details
        print(f"HTTP Error: {http_err}")
        print(f"API Response: {response.content}")
        return None

    except Exception as err:
        # Print general error details
        print(f"Error: {err}")
        return None


def display_top_activities(city_name, radius):
    """
    Display the top activities in a specified city within a given radius.

    Args:
        city_name (str): Name of the city to search for activities.
        radius (int): Search radius in kilometers.
    """
    # Search for activities in the specified city within the given radius
    activities_response = search_activities(city_name=city_name, radius=radius)

    if activities_response:
        # Extract the list of activities from the response dictionary
        activities = activities_response.get('data', [])

        # Display only the top 4 activities if they exist
        top_activities = activities[:4]
        for index, activity in enumerate(top_activities, start=1):
            print(f"Activity {index}: {activity['name']}")
            print(
                f"    Description: "
                f"{activity.get('shortDescription', 'No description available')}"
            )
            print(
                f"    Price: "
                f"{activity.get('price', 'Price information not available')}"
            )
            print(
                f"    Duration: "
                f"{activity.get('duration', 'Duration information not available')}"
            )
            print(
                f"    Location: "
                f"{activity.get('location', {}).get('address', 'Address not available')}"
            )
            print("")

    else:
        # Print a message if the activity search failed
        print("Activity search failed.")


# Example usage
if __name__ == "__main__":
    city_name = "Barcelona"
    radius = 1  # in kilometers

    # Display the top activities in the specified city and radius
    display_top_activities(city_name, radius)
