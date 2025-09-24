from flask import Flask, request, jsonify

app = Flask(__name__)

EXCHANGE_RATES = {
    'USD': 1.0,
    'EUR': 0.85,
    'DKK' : 6.37

}

@app.route('/convert', methods=['POST'])
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


app.run(port=5001)