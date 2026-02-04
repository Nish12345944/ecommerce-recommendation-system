from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import pandas as pd
import os
import random
from datetime import datetime
import json

app = Flask(__name__, template_folder='E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system-/templates')
# In-memory storage for demo
users = {}
cart_items = {}
orders = {}
wishlist = {}
reviews = {}
order_counter = 1000

# Sample products with prices
sample_products = [
    {'id': 1, 'name': 'Wireless Headphones', 'price': 99.99, 'category': 'Electronics', 'stock': 50},
    {'id': 2, 'name': 'Smartphone', 'price': 699.99, 'category': 'Electronics', 'stock': 30},
    {'id': 3, 'name': 'Running Shoes', 'price': 129.99, 'category': 'Fashion', 'stock': 25},
    {'id': 4, 'name': 'Coffee Maker', 'price': 89.99, 'category': 'Home', 'stock': 15},
    {'id': 5, 'name': 'Laptop Bag', 'price': 49.99, 'category': 'Accessories', 'stock': 40}
]

app.secret_key = 'your-secret-key-here'

# Load ML data
try:
    trending_products = pd.read_csv("E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system-/models/trending_products_corrected.csv")
    train_data = pd.read_csv("E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system-/models/clean_data.csv")
    train_data['Tags'] = train_data['Tags'].fillna('')
    train_data['Name'] = train_data['Name'].fillna('')
except Exception as e:
    print(f"Warning: Could not load ML data: {e}")
    trending_products = pd.DataFrame()
    train_data = pd.DataFrame()

def truncate(text, length):
    return text[:length] + "..." if len(str(text)) > length else str(text)

def get_recommendations(product_name, top_n=10):
    if train_data.empty:
        return pd.DataFrame()
    
    try:
        matches = train_data[train_data['Name'].str.contains(product_name, case=False, na=False)]
        if matches.empty:
            return train_data.head(top_n)
        return matches.head(top_n)
    except Exception as e:
        print(f"Recommendation error: {e}")
        return train_data.head(top_n)

@app.context_processor
def inject_user():
    user_id = session.get('user_id')
    cart_count = len(cart_items.get(user_id, [])) if user_id else 0
    return {'logged_in': bool(user_id), 'cart_count': cart_count, 'current_user': users.get(user_id)}

@app.route('/')
def index():
    return render_template('index.html', 
                         trending_products=trending_products.head(10),
                         truncate=truncate)

@app.route('/products')
def products():
    category = request.args.get('category')
    search = request.args.get('search')
    
    filtered_products = sample_products.copy()
    
    if category:
        filtered_products = [p for p in filtered_products if p['category'].lower() == category.lower()]
    
    if search:
        filtered_products = [p for p in filtered_products if search.lower() in p['name'].lower()]
    
    return render_template('products.html', products=filtered_products, categories=['Electronics', 'Fashion', 'Home', 'Accessories'])

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/main')
def main():
    return render_template('main.html', 
                         content_based_rec=pd.DataFrame(),
                         truncate=truncate)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user = users.get(session['user_id'])
    user_orders = orders.get(session['user_id'], [])
    return render_template('profile.html', user=user, orders=user_orders)

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user_cart = cart_items.get(session['user_id'], [])
    total = sum(item['price'] * item['quantity'] for item in user_cart)
    return render_template('cart.html', cart_items=user_cart, total=total)

# New Features
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('index'))
    
    product = next((p for p in sample_products if p['id'] == product_id), None)
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('products'))
    
    user_id = session['user_id']
    if user_id not in cart_items:
        cart_items[user_id] = []
    
    # Check if item already in cart
    existing = next((item for item in cart_items[user_id] if item['id'] == product_id), None)
    if existing:
        existing['quantity'] += 1
    else:
        cart_items[user_id].append({**product, 'quantity': 1})
    
    flash('Added to cart!', 'success')
    return redirect(request.referrer or url_for('products'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'user_id' in session:
        user_id = session['user_id']
        if user_id in cart_items:
            cart_items[user_id] = [item for item in cart_items[user_id] if item['id'] != product_id]
        flash('Removed from cart!', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user_cart = cart_items.get(session['user_id'], [])
    if not user_cart:
        flash('Cart is empty!', 'warning')
        return redirect(url_for('cart'))
    
    total = sum(item['price'] * item['quantity'] for item in user_cart)
    return render_template('checkout.html', cart_items=user_cart, total=total)

@app.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    global order_counter
    user_id = session['user_id']
    user_cart = cart_items.get(user_id, [])
    
    if not user_cart:
        flash('Cart is empty!', 'warning')
        return redirect(url_for('cart'))
    
    total = sum(item['price'] * item['quantity'] for item in user_cart)
    
    order = {
        'id': order_counter,
        'items': user_cart.copy(),
        'total': total,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'status': 'Processing'
    }
    
    if user_id not in orders:
        orders[user_id] = []
    orders[user_id].append(order)
    
    # Clear cart
    cart_items[user_id] = []
    order_counter += 1
    
    flash('Order placed successfully!', 'success')
    return redirect(url_for('order_success', order_id=order['id']))

@app.route('/order_success/<int:order_id>')
def order_success(order_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user_orders = orders.get(session['user_id'], [])
    order = next((o for o in user_orders if o['id'] == order_id), None)
    
    return render_template('order_success.html', order=order)

@app.route('/wishlist')
def view_wishlist():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user_wishlist = wishlist.get(session['user_id'], [])
    return render_template('wishlist.html', wishlist=user_wishlist)

@app.route('/add_to_wishlist/<int:product_id>')
def add_to_wishlist(product_id):
    if 'user_id' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('index'))
    
    product = next((p for p in sample_products if p['id'] == product_id), None)
    if product:
        user_id = session['user_id']
        if user_id not in wishlist:
            wishlist[user_id] = []
        
        if not any(item['id'] == product_id for item in wishlist[user_id]):
            wishlist[user_id].append(product)
            flash('Added to wishlist!', 'success')
        else:
            flash('Already in wishlist!', 'info')
    
    return redirect(request.referrer or url_for('products'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in sample_products if p['id'] == product_id), None)
    if not product:
        return redirect(url_for('products'))
    
    product_reviews = reviews.get(product_id, [])
    return render_template('product_detail.html', product=product, reviews=product_reviews)

@app.route('/add_review/<int:product_id>', methods=['POST'])
def add_review(product_id):
    if 'user_id' not in session:
        flash('Please login to add review!', 'warning')
        return redirect(url_for('product_detail', product_id=product_id))
    
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment', '')
    user = users.get(session['user_id'])
    
    if product_id not in reviews:
        reviews[product_id] = []
    
    reviews[product_id].append({
        'user': user['username'],
        'rating': rating,
        'comment': comment,
        'date': datetime.now().strftime('%Y-%m-%d')
    })
    
    flash('Review added!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))

# API Endpoints
@app.route('/api/products')
def api_products():
    return jsonify(sample_products)

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '')
    results = [p for p in sample_products if query.lower() in p['name'].lower()]
    return jsonify(results)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if username in users:
            flash('Username already exists!', 'error')
        else:
            user_id = len(users) + 1
            users[user_id] = {'username': username, 'email': email, 'password': password}
            flash('Registration successful!', 'success')
    return redirect(url_for('index'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('signinUsername')
        password = request.form.get('signinPassword')
        
        user = next((uid for uid, u in users.items() if u['username'] == username and u['password'] == password), None)
        
        if user:
            session['user_id'] = user
            flash('Welcome back!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid credentials!', 'error')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/recommendations', methods=['POST'])
def recommendations():
    query = request.form.get('prod', '').strip()
    if not query:
        flash('Please enter a search term.', 'warning')
        return redirect(url_for('search'))
    
    recommendations = get_recommendations(query)
    return render_template('search.html', 
                         recommendations=recommendations,
                         query=query,
                         truncate=truncate)

@app.route('/health')
def health_check():
    return {'status': 'healthy'}

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)