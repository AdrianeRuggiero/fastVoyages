from . import amadeus
from amadeus import Client, ResponseError


def search_flights(origin, budget):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            maxPrice=budget,
            currencyCode='EUR',
            max=5
        )
        return response.data
    except ResponseError as error:
        return {'error': str(error)}
