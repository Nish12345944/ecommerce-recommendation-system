# Project Structure

```
e-commerce_recommendation/
├── .github/
│   └── workflows/
│       └── ci-cd.yml                 # GitHub Actions CI/CD pipeline
├── E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system-/
│   ├── instance/
│   │   └── ecom.db                   # SQLite database
│   ├── models/
│   │   ├── clean_data.csv            # Processed product data
│   │   └── trending_products.csv     # Trending products data
│   ├── static/
│   │   ├── img/                      # Product images
│   │   └── v.mp4                     # Demo video
│   ├── templates/
│   │   ├── cart.html                 # Shopping cart page
│   │   ├── checkout.html             # Checkout page
│   │   ├── index.html                # Home page
│   │   ├── main.html                 # Search/recommendations page
│   │   ├── order_success.html        # Order confirmation
│   │   ├── product_detail.html       # Product details page
│   │   ├── products.html             # Product catalog
│   │   └── profile.html              # User profile page
│   ├── app.py                        # Main Flask application
│   ├── clean_names.py                # Data preprocessing script
│   ├── config.py                     # Configuration settings
│   └── recommendations code.ipynb    # ML model development
├── .dockerignore                     # Docker ignore file
├── .env                              # Environment variables
├── docker-compose.yml                # Docker Compose configuration
├── Dockerfile                        # Docker container definition
├── deploy.bat                        # Windows deployment script
├── deploy.sh                         # Linux/Mac deployment script
├── Makefile                          # Development commands
├── nginx.conf                        # Nginx configuration
├── README.md                         # Project documentation
├── requirements.txt                  # Python dependencies
└── test_app.py                       # Application tests
```

## Key Components

### Application Core
- **app.py**: Main Flask application with all routes and business logic
- **config.py**: Configuration management for different environments
- **requirements.txt**: Python package dependencies

### Machine Learning
- **models/**: Contains CSV data files for products and recommendations
- **recommendations code.ipynb**: Jupyter notebook for ML model development
- **clean_names.py**: Data preprocessing utilities

### Frontend
- **templates/**: HTML templates using Jinja2 templating
- **static/**: Static assets (images, CSS, JavaScript)

### Deployment
- **Dockerfile**: Container definition for the Flask app
- **docker-compose.yml**: Multi-container deployment configuration
- **nginx.conf**: Reverse proxy configuration
- **deploy.sh/deploy.bat**: Automated deployment scripts

### Development
- **Makefile**: Common development commands
- **test_app.py**: Unit tests for the application
- **.github/workflows/**: CI/CD pipeline configuration

### Configuration
- **.env**: Environment variables for configuration
- **.dockerignore**: Files to exclude from Docker build context

## Data Flow

1. **User Request** → Nginx (Port 80)
2. **Nginx** → Flask App (Port 5000)
3. **Flask App** → SQLite Database
4. **ML Engine** → Product Recommendations
5. **Response** → User Interface

## Deployment Options

1. **Docker Compose** (Recommended for production)
2. **Local Development** (For development and testing)
3. **Cloud Deployment** (AWS, GCP, Azure with container services)
4. **Kubernetes** (For large-scale deployments)

## Security Considerations

- Environment variables for sensitive data
- SQLite for development, PostgreSQL recommended for production
- Nginx for reverse proxy and static file serving
- HTTPS configuration ready for production
- Input validation and sanitization implemented