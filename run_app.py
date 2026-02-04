import os
import sys

# Add the main app directory to Python path
app_dir = os.path.join(os.path.dirname(__file__), 'E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system-')
sys.path.insert(0, app_dir)

# Change to the app directory
os.chdir(app_dir)

# Import and run the app
from app import app

if __name__ == '__main__':
    print("Starting E-Commerce Recommendation System...")
    print("Access the application at: http://localhost:8080")
    app.run(debug=True, host='127.0.0.1', port=8080)