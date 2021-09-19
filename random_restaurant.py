import requests
from random import randrange

API_KEY = "<API KEY>"
URL = "https://api.yelp.com/v3/businesses/search"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}


def generate_restaurant(zip_code):
    data = {
        "term": "restaurants",
        "location": zip_code,
        "limit": "50",
    }
    response = requests.get(url=URL, headers=headers, params=data)

    result = response.json()
    total = len(result["businesses"])
    random_index = randrange(total)

    name = result["businesses"][random_index]["name"]
    website = result["businesses"][random_index]["url"]
    category = result["businesses"][random_index]["categories"][0]["title"]
    rating = result["businesses"][random_index]["rating"]
    phone_number = result["businesses"][random_index]["display_phone"]
    address = result["businesses"][random_index]["location"]["display_address"]
    address = ' '.join(map(str, address))
    error_message = ""
    return name, website, category, rating, phone_number, address, error_message
