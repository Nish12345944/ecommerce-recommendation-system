from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd
import os

app = Flask(__name__, template_folder='E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system-/templates', static_folder='E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system-/static')
app.secret_key = 'your-secret-key'

# Load trending products
try:
    trending_products = pd.read_csv("E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system-/models/trending_products.csv")
except:
    trending_products = pd.DataFrame()

def truncate(text, length):
    if len(text) > length:
        return text[:length] + "..."
    else:
        return text

@app.route("/")
def index():
    return render_template('index.html', 
                         trending_products=trending_products.head(10),
                         truncate=truncate,
                         random_price=50,
                         cart_count=0, 
                         logged_in=False)

@app.route("/main")
def main():
    content_based_rec = pd.DataFrame()
    return render_template('main.html', 
                         content_based_rec=content_based_rec, 
                         truncate=truncate,
                         random_price=50,
                         cart_count=0, 
                         logged_in=False)

@app.route("/products")
def products():
    return render_template('products.html', 
                         products=[],
                         categories=[],
                         cart_count=0, 
                         logged_in=False)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        flash('Signup successful!', 'success')
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        flash('Signin successful!', 'success')
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route("/recommendations", methods=['GET', 'POST'])
def recommendations():
    if request.method == 'POST':
        return render_template('main.html', 
                             content_based_rec=pd.DataFrame(),
                             truncate=truncate,
                             random_price=50,
                             cart_count=0, 
                             logged_in=False,
                             message="Search functionality not implemented in simple app")
    return redirect(url_for('main'))

if __name__=='__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)