"""
    Account Service:
    Håndterer brugerkonti, herunder registrering, autentificering og profiladministration.
    Behandler login, logout, passwordhåndtering og brugerroller.
"""

from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from database import find_user_by_username, add_user
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('KEY')

jwt = JWTManager(app)

# Register en ny bruger
@app.route('/profile', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if find_user_by_username(username):
        return jsonify({'message': 'User already exists'}), 400

    add_user(username, password)
    return jsonify({'message': f'User registered successfully'}), 201

@app.route('/profile', methods=['GET'])
@jwt_required()
def view_profile():
    current_user = get_jwt_identity()

    user = find_user_by_username(current_user)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({'username': user['username'], 'id': user['id']}), 200

@app.route('/profile', methods=['PUT'])
@jwt_required()
def edit_profile():
    current_user = get_jwt_identity()
    # TODO: Implement profile editing logic
    return jsonify({'message': 'Profile update endpoint - not yet implemented', 'user': current_user}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    user = find_user_by_username(username)

    if not user or user['password'] != password:
        return jsonify({'message': 'Invalid username or password'}), 401

    # Create JWT token
    token = create_access_token(identity=username)

    response = make_response(jsonify({'message': 'Login successful'}), 200)
    response.headers['Authorization'] = f'Bearer {token}'
    return response

@app.route('/logout', methods=['POST'])
def logout():
    return jsonify(), 201


app.run(host='0.0.0.0', port=5000)