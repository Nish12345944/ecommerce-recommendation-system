# E-Commerce Recommendation System

A complete e-commerce platform with AI-powered product recommendations built with Flask, SQLAlchemy, and Machine Learning.

## Features

- **AI-Powered Recommendations**: Content-based filtering using TF-IDF and cosine similarity
- **User Authentication**: Secure signup/signin system
- **Shopping Cart**: Add/remove products with size and color options
- **Order Management**: Complete checkout process with order tracking
- **Product Catalog**: Browse products with filtering and search
- **Responsive Design**: Mobile-friendly Bootstrap UI
- **Admin Features**: Product management and user profiles

## Technology Stack

- **Backend**: Flask, SQLAlchemy, Python
- **Frontend**: HTML5, CSS3, Bootstrap 4, JavaScript
- **Machine Learning**: scikit-learn, pandas, numpy
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Deployment**: Docker, Docker Compose, Nginx

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git (to clone the repository)

### Deployment Options

#### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd e-commerce_recommendation
   ```

2. **Run deployment script**
   
   **Linux/Mac:**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```
   
   **Windows:**
   ```cmd
   deploy.bat
   ```

3. **Access the application**
   - Main application: http://localhost
   - Direct Flask access: http://localhost:5000

#### Option 2: Manual Docker Setup

1. **Build and start containers**
   ```bash
   docker-compose build
   docker-compose up -d
   ```

2. **View logs**
   ```bash
   docker-compose logs -f
   ```

3. **Stop the application**
   ```bash
   docker-compose down
   ```

#### Option 3: Local Development

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**
   ```bash
   export FLASK_APP=E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system-/app.py
   export FLASK_ENV=development
   ```

3. **Run the application**
   ```bash
   cd E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system-
   python app.py
   ```

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/ecom.db
DEBUG=False
PORT=5000
```

### Database Setup

The application automatically creates the SQLite database and populates it with sample data on first run.

## API Endpoints

### Authentication
- `POST /signup` - User registration
- `POST /signin` - User login
- `GET /logout` - User logout

### Products
- `GET /` - Home page with trending products
- `GET /products` - Product catalog with filtering
- `GET /product/<id>` - Product details
- `POST /recommendations` - Get product recommendations

### Shopping Cart
- `POST /add_to_cart/<id>` - Add product to cart
- `GET /cart` - View cart
- `GET /remove_from_cart/<id>` - Remove from cart

### Orders
- `GET /checkout` - Checkout page
- `POST /place_order` - Place order
- `GET /order_success/<id>` - Order confirmation

### User Profile
- `GET /profile` - User profile and order history

## Machine Learning Features

### Content-Based Recommendations

The system uses TF-IDF vectorization and cosine similarity to recommend products based on:
- Product descriptions and tags
- Brand similarity
- Category matching
- User search history

### Recommendation Algorithm

1. **Text Processing**: Clean and preprocess product descriptions
2. **Feature Extraction**: TF-IDF vectorization of product attributes
3. **Similarity Calculation**: Cosine similarity between products
4. **Ranking**: Sort recommendations by similarity score
5. **Filtering**: Apply user preferences and constraints

## Deployment Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │────│   Flask App     │────│   SQLite DB     │
│  (Port 80)      │    │  (Port 5000)    │    │   (Volume)      │
│  Load Balancer  │    │  Gunicorn       │    │   Persistent    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Production Considerations

### Security
- Change default secret key in production
- Use environment variables for sensitive data
- Implement HTTPS with SSL certificates
- Add rate limiting and input validation

### Database
- Migrate to PostgreSQL for production
- Implement database backups
- Add connection pooling

### Scaling
- Use Redis for session storage
- Implement caching for recommendations
- Add CDN for static assets
- Use container orchestration (Kubernetes)

### Monitoring
- Add application logging
- Implement health checks
- Monitor performance metrics
- Set up error tracking

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   docker-compose down
   # Or change ports in docker-compose.yml
   ```

2. **Database connection errors**
   ```bash
   # Ensure instance directory exists
   mkdir -p instance
   ```

3. **Permission denied on deploy.sh**
   ```bash
   chmod +x deploy.sh
   ```

### Logs and Debugging

```bash
# View application logs
docker-compose logs web

# View nginx logs
docker-compose logs nginx

# Access container shell
docker-compose exec web bash
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the logs for error details

## Acknowledgments

- Flask community for the excellent framework
- scikit-learn for machine learning capabilities
- Bootstrap for responsive UI components
- Docker for containerization support