"""
API Gateway:
Simple central entry point for all microservices.
Routes requests to appropriate services.
"""

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Service URLs (internal Docker network)
ACCOUNT_SERVICE_URL = "http://acc:5000"
CURRENCY_SERVICE_URL = "http://cur:5000"
PRODUCT_SERVICE_URL = "http://products:5000"


# Account Service routes
@app.route('/api/account/profile', methods=['POST'])
def register():
    response = requests.post(f"{ACCOUNT_SERVICE_URL}/profile", json=request.get_json())
    return jsonify(response.json()), response.status_code


@app.route('/api/account/profile', methods=['GET'])
def view_profile():
    auth_header = request.headers.get('Authorization')
    headers = {'Authorization': auth_header} if auth_header else {}
    response = requests.get(f"{ACCOUNT_SERVICE_URL}/profile", headers=headers)
    return jsonify(response.json()), response.status_code


@app.route('/api/account/profile', methods=['PUT'])
def edit_profile():
    response = requests.put(f"{ACCOUNT_SERVICE_URL}/profile")
    return jsonify(response.json()), response.status_code


@app.route('/api/account/login', methods=['POST'])
def login():
    response = requests.post(f"{ACCOUNT_SERVICE_URL}/login", json=request.get_json())
    # Forward the Authorization header from the response
    gateway_response = jsonify(response.json())
    if 'Authorization' in response.headers:
        return gateway_response, response.status_code, {'Authorization': response.headers['Authorization']}
    return gateway_response, response.status_code


@app.route('/api/account/logout', methods=['POST'])
def logout():
    response = requests.post(f"{ACCOUNT_SERVICE_URL}/logout")
    return jsonify(response.json()), response.status_code


# Product Service routes
@app.route('/api/products', methods=['GET'])
def get_products():
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products")
    return jsonify(response.json()), response.status_code


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    return jsonify(response.json()), response.status_code


@app.route('/api/products/search', methods=['GET'])
def search_products():
    query = request.args.get('title', '')
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products/search?title={query}")
    return jsonify(response.json()), response.status_code


@app.route('/api/products/category/<category_name>', methods=['GET'])
def get_products_by_category(category_name):
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products/category/{category_name}")
    return jsonify(response.json()), response.status_code


# Currency Service routes
@app.route('/api/currency/convert', methods=['POST'])
def convert_currency():
    response = requests.post(f"{CURRENCY_SERVICE_URL}/convert", json=request.get_json())
    return jsonify(response.json()), response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
