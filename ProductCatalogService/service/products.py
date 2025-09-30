import requests
import json

PRODUCTS_API_URL = 'https://dummyjson.com/products/category/smartphones'

def fetch_products():
    response = requests.get(PRODUCTS_API_URL)
    
    if response.status_code == 200:
        full_data = response.json()
        
        products = full_data if isinstance(full_data, list) else full_data.get('products', [])
        
        filtered_products = [
            {
                "brand": product["brand"],
                "category": product["category"],
                "description": product["description"],
                "dimensions": product["dimensions"],
                "id": product["id"],
                "images": product["images"],
                "org_price": product["price"],
                "dkk_price": _calculate_price(product["price"]),
                "tags": product["tags"],
                "thumbnail": product["thumbnail"],
                "title": product["title"],
                "weight": product["weight"]
            }
            for product in products
        ]
        
        return filtered_products
    return []

def _calculate_price(price):

    body = {
        "amount": price,
        "from_currency": "USD",
        "to_currency": "DKK"
    }
    response = requests.post('http://cur:5000/convert', json=body)
    
    if response.status_code == 200:
        data = response.json()
        return data['converted_amount']
    
    return None

