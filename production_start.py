"""
Production startup script for E-commerce Recommendation System
Handles initialization, validation, and graceful error handling
"""

import os
import sys
import logging
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / 'E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system-'
sys.path.insert(0, str(app_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('startup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'flask', 'pandas', 'numpy', 
        'rapidfuzz', 'nltk', 'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'rapidfuzz':
                import rapidfuzz
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing required packages: {missing_packages}")
        logger.info("Install missing packages with: pip install -r requirements.txt")
        return False
    
    return True

def validate_data_files():
    """Validate that required data files exist"""
    required_files = [
        app_dir / 'models' / 'trending_products.csv',
        app_dir / 'models' / 'clean_data.csv'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not file_path.exists():
            missing_files.append(str(file_path))
    
    if missing_files:
        logger.error(f"Missing required data files: {missing_files}")
        return False
    
    return True

def download_nltk_data():
    """Download required NLTK data"""
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        logger.info("NLTK data downloaded successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to download NLTK data: {e}")
        return False

def initialize_components():
    """Initialize and validate all system components"""
    try:
        # Change to app directory
        os.chdir(app_dir)
        
        # Import and initialize app
        from app import app, product_manager, search_engine, recommendation_engine
        
        # Validate components
        if not product_manager:
            logger.warning("Product manager not initialized - some features may be limited")
        
        if not search_engine:
            logger.warning("Search engine not initialized - search may be limited")
        
        if not recommendation_engine:
            logger.warning("Recommendation engine not initialized - recommendations may be limited")
        
        # Test database connection
        with app.app_context():
            from app import db
            db.create_all()
            logger.info("Database initialized successfully")
        
        logger.info("All components initialized successfully")
        return app
        
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        return None

def main():
    """Main startup function"""
    logger.info("Starting E-commerce Recommendation System...")
    
    # Step 1: Check dependencies
    logger.info("Checking dependencies...")
    if not check_dependencies():
        logger.error("Dependency check failed. Exiting.")
        sys.exit(1)
    
    # Step 2: Validate data files
    logger.info("Validating data files...")
    if not validate_data_files():
        logger.error("Data file validation failed. Exiting.")
        sys.exit(1)
    
    # Step 3: Download NLTK data
    logger.info("Downloading NLTK data...")
    if not download_nltk_data():
        logger.warning("NLTK data download failed - some features may be limited")
    
    # Step 4: Initialize components
    logger.info("Initializing system components...")
    app = initialize_components()
    
    if not app:
        logger.error("Component initialization failed. Exiting.")
        sys.exit(1)
    
    # Step 5: Start the application
    logger.info("Starting Flask application...")
    
    # Get configuration from environment
    debug_mode = os.getenv('DEBUG', 'True').lower() == 'true'
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('HOST', '127.0.0.1')
    
    logger.info(f"Server starting on http://{host}:{port}")
    logger.info(f"Debug mode: {debug_mode}")
    
    try:
        app.run(debug=debug_mode, host=host, port=port)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()