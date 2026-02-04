import os
import sys

# Add the app directory to path
app_dir = os.path.join(os.path.dirname(__file__), 'E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system-')
sys.path.insert(0, app_dir)
os.chdir(app_dir)

from app import app, db, Signup
from werkzeug.security import generate_password_hash

def test_database():
    with app.app_context():
        try:
            # Test database connection
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Test user creation
            test_user = Signup(
                username='testuser',
                email='test@example.com',
                password=generate_password_hash('testpass123')
            )
            
            # Check if user already exists
            existing = Signup.query.filter_by(username='testuser').first()
            if existing:
                print("✅ Test user already exists")
            else:
                db.session.add(test_user)
                db.session.commit()
                print("✅ Test user created successfully")
            
            # Test user query
            user = Signup.query.filter_by(username='testuser').first()
            if user:
                print(f"✅ User found: {user.username}, {user.email}")
            else:
                print("❌ User not found")
                
            print("✅ Database operations working correctly")
            return True
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False

if __name__ == '__main__':
    success = test_database()
    if success:
        print("\n🚀 Starting Flask app...")
        app.run(debug=True, host='127.0.0.1', port=8080)
    else:
        print("\n❌ Database test failed. Please check the error above.")