from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Ecommerce RecSys API is running on port 9000!'})

@app.route('/api/products')
def products():
    return jsonify([
        {'id': 1, 'name': 'Headphones', 'price': 79.99},
        {'id': 2, 'name': 'Smart Watch', 'price': 199.99}
    ])

if __name__ == '__main__':
    app.run(debug=True, port=9000, host='127.0.0.1')