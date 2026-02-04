import os
import sys

# Add the app directory to path
app_dir = os.path.join(os.path.dirname(__file__), 'E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system-')
sys.path.insert(0, app_dir)
os.chdir(app_dir)

from app import app, db, Signup
from werkzeug.security import generate_password_hash

print("Testing database operations...")

with app.app_context():
    try:
        # Create tables
        db.create_all()
        print("✅ Tables created")
        
        # Test user creation
        test_user = Signup(
            username='testuser123',
            email='test123@example.com',
            password=generate_password_hash('password123')
        )
        
        db.session.add(test_user)
        db.session.commit()
        print("✅ User created successfully")
        
        # Verify user exists
        user = Signup.query.filter_by(username='testuser123').first()
        if user:
            print(f"✅ User verified: {user.username}")
        else:
            print("❌ User not found after creation")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

print("Database test complete")