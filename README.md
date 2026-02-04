# E-Commerce Recommendation System

A complete e-commerce platform with AI-powered product recommendations built with Flask, SQLAlchemy, and Machine Learning. Features both traditional Flask web app and modern React frontend options.

## 🚀 Features

- **AI-Powered Recommendations**: Content-based filtering using TF-IDF and cosine similarity
- **Dual Frontend Options**: Traditional Flask templates + Modern React SPA
- **User Authentication**: Secure signup/signin with session management
- **Shopping Cart**: Add/remove products with persistent cart state
- **Order Management**: Complete checkout process with order tracking
- **Product Catalog**: Browse products with filtering, search, and pagination
- **Responsive Design**: Mobile-friendly Bootstrap UI + Tailwind CSS
- **Production Ready**: Rate limiting, caching, security headers
- **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions
- **API Endpoints**: RESTful API for frontend integration

## 🛠 Technology Stack

- **Backend**: Flask, SQLAlchemy, Python 3.9+
- **Frontend**: HTML5/Bootstrap 4 + React/Tailwind CSS
- **Machine Learning**: scikit-learn, pandas, numpy, NLTK
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Deployment**: Docker, Docker Compose, Nginx, Gunicorn
- **Security**: Flask-Limiter, Werkzeug security, CSRF protection
- **Caching**: Flask-Caching with memoization
- **State Management**: Zustand (React frontend)

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
   - Health check: http://localhost:5000/health

#### Option 2: Production Deployment

1. **Use production configuration**
   ```bash
   chmod +x deploy_production.sh
   ./deploy_production.sh
   ```

2. **Production features**
   - Gunicorn WSGI server
   - Nginx reverse proxy
   - Rate limiting and security headers
   - Production logging and monitoring

#### Option 3: React Frontend (Modern SPA)

1. **Backend setup**
   ```bash
   cd ecommerce-recsys/backend
   pip install -r requirements.txt
   python app.py
   ```

2. **Frontend setup**
   ```bash
   cd ecommerce-recsys/frontend
   npm install
   npm start
   ```

3. **Access applications**
   - React frontend: http://localhost:3000
   - Flask API: http://localhost:5000

#### Option 4: Local Development

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run with different configurations**
   ```bash
   # Simple development server
   python app_simple.py
   
   # Production-ready server
   python app_production.py
   
   # Minimal testing server
   python app_minimal.py
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

## 📡 API Endpoints

### Authentication
- `POST /signup` - User registration with validation
- `POST /signin` - User login with rate limiting
- `GET /logout` - User logout and session cleanup

### Products
- `GET /` - Home page with trending products
- `GET /products` - Product catalog with filtering and pagination
- `GET /product/<id>` - Product details with related products
- `POST /recommendations` - AI-powered product recommendations
- `GET /api/products` - JSON API for product data

### Shopping Cart
- `POST /add_to_cart/<id>` - Add product to cart with stock validation
- `GET /cart` - View cart with total calculation
- `GET /remove_from_cart/<id>` - Remove from cart

### Orders
- `GET /checkout` - Checkout page with cart validation
- `POST /place_order` - Place order with inventory management
- `GET /order_success/<id>` - Order confirmation page

### User Profile
- `GET /profile` - User profile and order history
- `GET /wishlist` - User wishlist management

### System
- `GET /health` - Health check endpoint for monitoring
- `GET /search` - Advanced search functionality

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

## 🏗 Project Architecture

### Traditional Flask App
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │────│   Flask App     │────│   SQLite DB     │
│  (Port 80)      │    │  (Port 5000)    │    │   (Volume)      │
│  Load Balancer  │    │  Gunicorn       │    │   Persistent    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Modern React + Flask API
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React SPA     │────│   Flask API     │────│   SQLite DB     │
│  (Port 3000)    │    │  (Port 5000)    │    │   (Volume)      │
│  Tailwind CSS   │    │  CORS Enabled   │    │   Persistent    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### CI/CD Pipeline
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  GitHub Actions │────│   Docker Build  │────│   Deployment    │
│  Automated Tests│    │   Multi-stage   │    │   Production    │
│  Code Quality   │    │   Optimization  │    │   Monitoring    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 Production Features

### Security
- ✅ Rate limiting with Flask-Limiter (200/day, 50/hour)
- ✅ Secure session management with HTTPOnly cookies
- ✅ Password hashing with Werkzeug security
- ✅ Input validation and sanitization
- ✅ CSRF protection and security headers
- ✅ Environment-based configuration

### Performance
- ✅ Caching with Flask-Caching and memoization
- ✅ Database query optimization with indexes
- ✅ Gunicorn WSGI server for production
- ✅ Nginx reverse proxy and static file serving
- ✅ Docker multi-stage builds for optimization

### Monitoring & Logging
- ✅ Health check endpoints
- ✅ Structured logging with different levels
- ✅ Error handling with custom error pages
- ✅ Request/response logging
- ✅ Performance metrics tracking

### Scalability
- ✅ Containerized deployment with Docker
- ✅ Horizontal scaling ready
- ✅ Database migration support
- ✅ Environment-specific configurations
- 🔄 Redis integration (planned)
- 🔄 PostgreSQL migration (planned)
- 🔄 Kubernetes deployment (planned)

## 🔍 Development & Testing

### Available Scripts

```bash
# Development commands
make install          # Install dependencies
make run             # Run development server
make test            # Run tests
make clean           # Clean build artifacts

# Docker commands
make docker-build    # Build Docker image
make docker-run      # Run Docker container
make docker-logs     # View container logs
```

### Testing

```bash
# Run unit tests
python -m pytest test_app.py -v

# Run authentication tests
python test_auth.py

# Test database operations
python debug_db.py
```

### Troubleshooting

#### Common Issues

1. **Port already in use**
   ```bash
   docker-compose down
   # Or change ports in docker-compose.yml
   ```

2. **Database connection errors**
   ```bash
   # Ensure instance directory exists
   mkdir -p instance
   # Check database initialization
   python debug_db.py
   ```

3. **Permission denied on deploy scripts**
   ```bash
   chmod +x deploy.sh deploy_production.sh
   ```

4. **React frontend issues**
   ```bash
   cd ecommerce-recsys/frontend
   npm install
   npm audit fix
   ```

#### Logs and Debugging

```bash
# View application logs
docker-compose logs -f web

# View nginx logs
docker-compose logs -f nginx

# Access container shell
docker-compose exec web bash

# Check application health
curl http://localhost:5000/health
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

## 📁 Project Structure

```
e-commerce_recommendation/
├── .github/workflows/           # CI/CD pipeline
├── ecommerce-recsys/           # Modern React + Flask API
│   ├── backend/                # Flask REST API
│   └── frontend/               # React SPA with Tailwind
├── E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system-/
│   ├── templates/              # Flask HTML templates
│   ├── static/                 # Static assets
│   ├── models/                 # ML data and models
│   └── app.py                  # Main Flask application
├── docker-compose.yml          # Development deployment
├── docker-compose_production.yml # Production deployment
├── Dockerfile                  # Container definition
├── requirements.txt            # Python dependencies
├── deploy.sh / deploy.bat      # Deployment scripts
├── Makefile                    # Development commands
└── README.md                   # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Run the test suite (`make test`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- 📧 Create an issue in the repository
- 📖 Check the troubleshooting section
- 🔍 Review the logs for error details
- 💬 Check existing discussions and issues

## 🙏 Acknowledgments

- **Flask** community for the excellent framework
- **scikit-learn** for machine learning capabilities
- **React** and **Tailwind CSS** for modern frontend
- **Bootstrap** for responsive UI components
- **Docker** for containerization support
- **GitHub Actions** for CI/CD automation
- **Nginx** for production-ready deployment