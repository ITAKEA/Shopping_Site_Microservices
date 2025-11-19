from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('KEY')

jwt = JWTManager(app)

EXCHANGE_RATES = {
    'USD': 1.0,
    'EUR': 0.85,
    'DKK' : 6.37

}

@app.route('/convert', methods=['POST'])
@jwt_required()
def convert_currency():
        data = request.get_json()
        amount = data.get('amount')
        from_currency = data.get('from_currency', '').upper()
        to_currency = data.get('to_currency', '').upper()

        usd_amount = amount / EXCHANGE_RATES[from_currency]
        converted_amount = usd_amount * EXCHANGE_RATES[to_currency]

        return jsonify({
            'original_amount': amount,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'converted_amount': round(converted_amount, 2),
            'exchange_rate': round(EXCHANGE_RATES[to_currency] / EXCHANGE_RATES[from_currency], 4)
        }), 200


app.run(host='0.0.0.0', port=5000)