import unittest
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system-'))

from app import app, db

class BasicTestCase(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        with app.app_context():
            db.drop_all()
    
    def test_home_page(self):
        """Test that home page loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ecommerce RecSys', response.data)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'healthy', response.data)
    
    def test_products_page(self):
        """Test products page loads"""
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)
    
    def test_main_page(self):
        """Test main/search page loads"""
        response = self.app.get('/main')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()