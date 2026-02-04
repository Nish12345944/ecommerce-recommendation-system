import os
import logging
from datetime import datetime, timedelta
from functools import wraps
import secrets
import hashlib
import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, render_template, session, redirect, url_for, flash, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix

# Initialize Flask app
app = Flask(__name__)

# Production configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///ecommerce.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

app.config.from_object(Config)

# Production middleware
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cache = Cache(app)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

# Configure logging
if not app.debug:
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    brand = db.Column(db.String(100), index=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), index=True)
    image_url = db.Column(db.String(500))
    stock = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    tags = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Load ML data
try:
    trending_products = pd.read_csv("models/trending_products.csv")
    train_data = pd.read_csv("models/clean_data.csv")
    train_data['Tags'] = train_data['Tags'].fillna('')
    train_data['Name'] = train_data['Name'].fillna('')
except Exception as e:
    app.logger.error(f"Error loading ML data: {e}")
    trending_products = pd.DataFrame()
    train_data = pd.DataFrame()

# Utility functions
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('signin'))
        return f(*args, **kwargs)
    return decorated_function

def truncate(text, length):
    return text[:length] + "..." if len(str(text)) > length else str(text)

@cache.memoize(timeout=300)
def get_recommendations(product_name, top_n=10):
    """Get product recommendations using ML"""
    if train_data.empty:
        return pd.DataFrame()
    
    try:
        # Find product
        matches = train_data[train_data['Name'].str.contains(product_name, case=False, na=False)]
        if matches.empty:
            return train_data.head(top_n)
        
        # TF-IDF similarity
        tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
        tfidf_matrix = tfidf.fit_transform(train_data['Tags'].fillna(''))
        
        idx = matches.index[0]
        cosine_sim = cosine_similarity(tfidf_matrix[idx:idx+1], tfidf_matrix).flatten()
        similar_indices = cosine_sim.argsort()[-top_n-1:-1][::-1]
        
        return train_data.iloc[similar_indices]
    except Exception as e:
        app.logger.error(f"Recommendation error: {e}")
        return train_data.head(top_n)

# Context processors
@app.context_processor
def inject_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        cart_count = Cart.query.filter_by(user_id=user_id).count()
        return {'logged_in': True, 'current_user': user, 'cart_count': cart_count}
    return {'logged_in': False, 'cart_count': 0}

# Routes
@app.route('/')
@cache.cached(timeout=300)
def index():
    featured_products = Product.query.filter_by(is_active=True).limit(8).all()
    return render_template('index.html', 
                         trending_products=trending_products.head(10),
                         featured_products=featured_products,
                         truncate=truncate)

@app.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = Product.query.filter_by(is_active=True)
    
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Product.name.contains(search))
    
    products = query.paginate(page=page, per_page=12, error_out=False)
    categories = db.session.query(Product.category).distinct().all()
    
    return render_template('products.html', products=products, categories=categories)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related = Product.query.filter_by(category=product.category).filter(Product.id != product_id).limit(4).all()
    return render_template('product_detail.html', product=product, related_products=related)

@app.route('/signup', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Validation
        if not all([username, email, password]):
            flash('All fields are required.', 'error')
            return redirect(url_for('index'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return redirect(url_for('index'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('index'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('index'))
        
        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please sign in.', 'success')
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/signin', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def signin():
    if request.method == 'POST':
        username = request.form.get('signinUsername', '').strip()
        password = request.form.get('signinPassword', '')
        
        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('index'))
        
        user = User.query.filter_by(username=username, is_active=True).first()
        
        if user and user.check_password(password):
            session.permanent = True
            session['user_id'] = user.id
            user.last_login = datetime.utcnow()
            db.session.commit()
            flash('Welcome back!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid credentials.', 'error')
            return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    return render_template('profile.html', user=user, orders=orders)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
@limiter.limit("30 per minute")
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    
    if product.stock <= 0:
        flash('Product out of stock.', 'error')
        return redirect(request.referrer or url_for('products'))
    
    cart_item = Cart.query.filter_by(user_id=session['user_id'], product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(user_id=session['user_id'], product_id=product_id)
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Item added to cart!', 'success')
    return redirect(request.referrer or url_for('products'))

@app.route('/cart')
@login_required
def cart():
    cart_items = db.session.query(Cart, Product).join(Product).filter(Cart.user_id == session['user_id']).all()
    total = sum(item.Product.price * item.Cart.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout')
@login_required
def checkout():
    cart_items = db.session.query(Cart, Product).join(Product).filter(Cart.user_id == session['user_id']).all()
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('cart'))
    
    total = sum(item.Product.price * item.Cart.quantity for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/place_order', methods=['POST'])
@login_required
@limiter.limit("5 per minute")
def place_order():
    cart_items = Cart.query.filter_by(user_id=session['user_id']).all()
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('cart'))
    
    total = sum(Product.query.get(item.product_id).price * item.quantity for item in cart_items)
    
    order = Order(user_id=session['user_id'], total_amount=total)
    db.session.add(order)
    
    # Clear cart
    Cart.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    
    flash('Order placed successfully!', 'success')
    return redirect(url_for('order_success', order_id=order.id))

@app.route('/order_success/<int:order_id>')
@login_required
def order_success(order_id):
    order = Order.query.filter_by(id=order_id, user_id=session['user_id']).first_or_404()
    return render_template('order_success.html', order=order)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/recommendations', methods=['POST'])
@limiter.limit("20 per minute")
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

# API Routes
@app.route('/api/products')
@limiter.limit("100 per minute")
def api_products():
    products = Product.query.filter_by(is_active=True).limit(50).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'category': p.category,
        'rating': p.rating
    } for p in products])

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded'}), 429

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create sample products if none exist
        if Product.query.count() == 0:
            sample_products = [
                Product(name="Wireless Headphones", brand="TechBrand", price=99.99, category="Electronics", 
                       description="High-quality wireless headphones", stock=50, rating=4.5, review_count=120),
                Product(name="Smartphone", brand="PhoneCorp", price=699.99, category="Electronics",
                       description="Latest smartphone with advanced features", stock=30, rating=4.7, review_count=89),
                Product(name="Running Shoes", brand="SportWear", price=129.99, category="Fashion",
                       description="Comfortable running shoes", stock=25, rating=4.3, review_count=67)
            ]
            
            for product in sample_products:
                db.session.add(product)
            
            db.session.commit()
            app.logger.info("Sample products created")

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)