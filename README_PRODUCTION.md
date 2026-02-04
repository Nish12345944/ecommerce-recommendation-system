# E-Commerce Recommendation System - Production Ready

A complete, production-ready e-commerce platform with AI-powered product recommendations built with Flask, PostgreSQL, Redis, and Machine Learning.

## 🚀 Quick Production Deployment

### Prerequisites
- Docker & Docker Compose
- 4GB+ RAM
- 10GB+ disk space

### One-Click Deployment

**Linux/Mac:**
```bash
chmod +x deploy_production.sh
./deploy_production.sh
```

**Windows:**
```cmd
deploy_production.bat
```

**Access your application:**
- HTTP: http://localhost
- HTTPS: https://localhost
- API: http://localhost/api/products
- Health Check: http://localhost/health

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │────│   Flask App     │────│   PostgreSQL    │
│  Load Balancer  │    │   (Gunicorn)    │    │   Database      │
│   SSL/Security  │    │   Rate Limited  │    │   Persistent    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────│     Redis       │──────────────┘
                        │   Cache/Session │
                        └─────────────────┘
```

## 🔧 Production Features

### Security
- ✅ Rate limiting (API & Auth endpoints)
- ✅ HTTPS/SSL encryption
- ✅ Security headers (HSTS, XSS protection)
- ✅ Password hashing (Werkzeug)
- ✅ Session security
- ✅ Input validation & sanitization
- ✅ CSRF protection

### Performance
- ✅ Redis caching
- ✅ Database connection pooling
- ✅ Gzip compression
- ✅ Static file optimization
- ✅ ML model caching
- ✅ Pagination
- ✅ Lazy loading

### Scalability
- ✅ Horizontal scaling ready
- ✅ Load balancing (Nginx)
- ✅ Database migrations
- ✅ Container orchestration
- ✅ Health checks
- ✅ Graceful shutdowns

### Monitoring
- ✅ Application logging
- ✅ Health endpoints
- ✅ Error tracking
- ✅ Performance metrics
- ✅ Database monitoring

## 🛠️ Configuration

### Environment Variables (.env)
```env
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this
DATABASE_URL=postgresql://user:pass@db:5432/ecommerce
REDIS_URL=redis://redis:6379/0

# Security
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true

# Email (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# AWS S3 (Optional)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_BUCKET=your-bucket
```

### Database Configuration
- **Development:** SQLite (automatic)
- **Production:** PostgreSQL (recommended)
- **Migrations:** Flask-Migrate
- **Connection Pooling:** SQLAlchemy

### Caching Strategy
- **Session Storage:** Redis
- **ML Recommendations:** In-memory + Redis
- **Static Files:** Nginx + Browser cache
- **Database Queries:** Redis cache

## 📊 API Endpoints

### Public Endpoints
```
GET  /                    # Home page
GET  /products           # Product catalog
GET  /product/<id>       # Product details
GET  /search            # Search page
POST /recommendations   # Get recommendations
GET  /health           # Health check
```

### Authentication
```
POST /signup           # User registration
POST /signin           # User login
GET  /logout          # User logout
```

### User Dashboard
```
GET  /profile         # User profile
GET  /cart           # Shopping cart
POST /add_to_cart/<id> # Add to cart
GET  /checkout       # Checkout page
POST /place_order    # Place order
```

### API (JSON)
```
GET  /api/products    # Products API
```

## 🔍 Machine Learning Features

### Recommendation Engine
- **Algorithm:** Content-based filtering
- **Technology:** TF-IDF + Cosine similarity
- **Features:** Product descriptions, tags, categories
- **Caching:** 5-minute cache for performance
- **Fallback:** Popular products when no matches

### Data Processing
- **Input:** CSV files (trending_products.csv, clean_data.csv)
- **Processing:** Pandas + NumPy
- **Vectorization:** Scikit-learn TF-IDF
- **Similarity:** Cosine similarity matrix

## 🚀 Deployment Options

### 1. Docker Compose (Recommended)
```bash
# Production deployment
docker-compose -f docker-compose_production.yml up -d

# Development
docker-compose up -d
```

### 2. Kubernetes
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/
```

### 3. Cloud Platforms

#### AWS ECS
```bash
# Deploy to AWS ECS
aws ecs create-service --cli-input-json file://ecs-service.json
```

#### Google Cloud Run
```bash
# Deploy to Cloud Run
gcloud run deploy --image gcr.io/PROJECT/ecommerce-app
```

#### Azure Container Instances
```bash
# Deploy to Azure
az container create --resource-group myResourceGroup --file docker-compose_production.yml
```

## 🔧 Development Setup

### Local Development
```bash
# Clone repository
git clone <repository-url>
cd e-commerce_recommendation

# Install dependencies
pip install -r requirements_production.txt

# Set environment variables
export FLASK_APP=app_production.py
export FLASK_ENV=development

# Initialize database
python -c "from app_production import init_db; init_db()"

# Run application
python app_production.py
```

### Testing
```bash
# Run tests
python -m pytest tests/

# Load testing
ab -n 1000 -c 10 http://localhost:5000/

# Security testing
bandit -r app_production.py
```

## 📈 Performance Optimization

### Database Optimization
- Indexed columns (username, email, category)
- Connection pooling
- Query optimization
- Pagination for large datasets

### Caching Strategy
- Redis for session storage
- ML model result caching
- Static file caching (1 year)
- Database query caching

### Frontend Optimization
- Minified CSS/JS
- Image optimization
- Lazy loading
- CDN integration ready

## 🔒 Security Best Practices

### Authentication & Authorization
- Password hashing (Werkzeug)
- Session management
- Rate limiting (5 login attempts/minute)
- CSRF protection

### Data Protection
- Input validation
- SQL injection prevention
- XSS protection
- Secure headers

### Infrastructure Security
- HTTPS enforcement
- Security headers
- Container security
- Network isolation

## 📊 Monitoring & Logging

### Application Monitoring
```python
# Health check endpoint
GET /health
Response: {"status": "healthy", "timestamp": "2024-01-01T00:00:00"}
```

### Logging Configuration
- Production: INFO level
- Development: DEBUG level
- Error tracking ready
- Performance metrics

### Metrics Collection
- Request/response times
- Error rates
- Database performance
- Cache hit rates

## 🔄 Backup & Recovery

### Database Backups
```bash
# Automated backup
docker-compose exec db pg_dump -U postgres ecommerce > backup.sql

# Restore
docker-compose exec db psql -U postgres ecommerce < backup.sql
```

### File Backups
- Application code (Git)
- User uploads (S3/Cloud storage)
- Configuration files
- SSL certificates

## 🚨 Troubleshooting

### Common Issues

#### Application won't start
```bash
# Check logs
docker-compose -f docker-compose_production.yml logs web

# Check database connection
docker-compose exec web python -c "from app_production import db; print(db.engine.url)"
```

#### Performance issues
```bash
# Check resource usage
docker stats

# Monitor database
docker-compose exec db psql -U postgres -c "SELECT * FROM pg_stat_activity;"
```

#### SSL/HTTPS issues
```bash
# Generate new certificates
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes
```

### Support
- Check logs: `docker-compose logs -f`
- Database issues: Check PostgreSQL logs
- Performance: Monitor Redis and database connections
- Security: Review Nginx access logs

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

---

**Production Ready Features:**
✅ Scalable architecture  
✅ Security hardened  
✅ Performance optimized  
✅ Monitoring enabled  
✅ Backup strategy  
✅ CI/CD ready  
✅ Cloud deployment ready  
✅ Documentation complete