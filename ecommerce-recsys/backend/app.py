from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample products data
products = [
    {
        'id': 1,
        'name': 'Wireless Bluetooth Headphones',
        'brand': 'TechSound',
        'price': 79.99,
        'original_price': 99.99,
        'description': 'High-quality wireless headphones with noise cancellation',
        'category': 'electronics',
        'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
        'rating': 4.5,
        'review_count': 128,
        'stock': 25,
        'sizes': ['One Size'],
        'colors': ['Black', 'White', 'Blue']
    },
    {
        'id': 2,
        'name': 'Smart Fitness Watch',
        'brand': 'FitTech',
        'price': 199.99,
        'description': 'Advanced fitness tracking with heart rate monitor',
        'category': 'electronics',
        'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400',
        'rating': 4.7,
        'review_count': 89,
        'stock': 15,
        'sizes': ['S', 'M', 'L'],
        'colors': ['Black', 'Silver', 'Rose Gold']
    },
    {
        'id': 3,
        'name': 'Premium Coffee Mug',
        'brand': 'BrewMaster',
        'price': 24.99,
        'description': 'Ceramic coffee mug with temperature retention',
        'category': 'home',
        'image_url': 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400',
        'rating': 4.3,
        'review_count': 45,
        'stock': 50,
        'sizes': ['12oz', '16oz'],
        'colors': ['White', 'Black', 'Blue']
    },
    {
        'id': 4,
        'name': 'Laptop Stand',
        'brand': 'DeskPro',
        'price': 49.99,
        'description': 'Adjustable aluminum laptop stand for better ergonomics',
        'category': 'electronics',
        'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400',
        'rating': 4.6,
        'review_count': 67,
        'stock': 30,
        'sizes': ['One Size'],
        'colors': ['Silver', 'Space Gray']
    }
]

# Routes
@app.route('/')
def home():
    return jsonify({'message': 'Ecommerce RecSys API is running!'})

@app.route('/api/products')
def get_products():
    category = request.args.get('category')
    search = request.args.get('search')
    
    filtered_products = products
    
    if category:
        filtered_products = [p for p in filtered_products if p['category'] == category]
    
    if search:
        filtered_products = [p for p in filtered_products if search.lower() in p['name'].lower()]
    
    return jsonify(filtered_products)

@app.route('/api/products/<int:product_id>')
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

@app.route('/api/products/trending')
def get_trending():
    return jsonify(sorted(products, key=lambda x: x['rating'], reverse=True)[:3])

@app.route('/api/recommendations/product/<int:product_id>')
def get_recommendations(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        # Simple recommendation: same category, different product
        recommendations = [p for p in products if p['category'] == product['category'] and p['id'] != product_id]
        return jsonify(recommendations[:3])
    return jsonify([])

@app.route('/api/recommendations/user/<int:user_id>')
def get_user_recommendations(user_id):
    # Return top rated products as user recommendations
    return jsonify(sorted(products, key=lambda x: x['rating'], reverse=True)[:4])

if __name__ == '__main__':
    print("Starting Ecommerce RecSys Backend on http://localhost:5000")
    app.run(debug=True, port=5000)