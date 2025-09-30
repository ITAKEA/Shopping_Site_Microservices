"""
Product Catalog Service:
Styrer listen over tilgængelige produkter, inklusive detaljer såsom navn, beskrivelse, pris og billeder.
Tilbyder funktionalitet til at søge, filtrere og kategorisere produkter.
"""
from flask import Flask, jsonify, request
from service.products import fetch_products

app = Flask(__name__)

@app.route('/products', methods=['GET'])
def get_all_products():
    products = fetch_products()
    return jsonify(products)

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    products = fetch_products()
    
    return jsonify([product for product in products if product['id'] == id])

# Søg efter products på title
@app.route('/products/search', methods=['GET'])
def search_products():
    query = request.args.get('title', '').lower()
    products = fetch_products()
    
    filtered_products = [product for product in products if query in product['title'].lower()]
    return jsonify(filtered_products)

@app.route('/products/category/<category_name>', methods=['GET'])
def get_products_by_category(category_name):
    products = fetch_products()
    
    filtered_products = [product for product in products if product['category'].lower() == category_name.lower()]
    return jsonify(filtered_products)


app.run(host='0.0.0.0', port=5000)