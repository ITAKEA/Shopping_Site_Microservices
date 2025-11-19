"""
Product Catalog Service:
Styrer listen over tilgængelige produkter, inklusive detaljer såsom navn, beskrivelse, pris og billeder.
Tilbyder funktionalitet til at søge, filtrere og kategorisere produkter.
"""
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from service.products import fetch_products
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('KEY')

jwt = JWTManager(app)

@app.route('/products', methods=['GET'])
@jwt_required()
def get_all_products():
    # Get the Authorization token from request headers to pass to currency service
    auth_token = request.headers.get('Authorization')
    products = fetch_products(auth_token)
    return jsonify(products)

@app.route('/products/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    auth_token = request.headers.get('Authorization')
    products = fetch_products(auth_token)

    return jsonify([product for product in products if product['id'] == id])

# Søg efter products på title
@app.route('/products/search', methods=['GET'])
@jwt_required()
def search_products():
    query = request.args.get('title', '').lower()
    auth_token = request.headers.get('Authorization')
    products = fetch_products(auth_token)

    filtered_products = [product for product in products if query in product['title'].lower()]
    return jsonify(filtered_products)

@app.route('/products/category/<category_name>', methods=['GET'])
@jwt_required()
def get_products_by_category(category_name):
    auth_token = request.headers.get('Authorization')
    products = fetch_products(auth_token)

    filtered_products = [product for product in products if product['category'].lower() == category_name.lower()]
    return jsonify(filtered_products)


app.run(host='0.0.0.0', port=5000)