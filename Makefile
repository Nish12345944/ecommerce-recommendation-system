.PHONY: help install run test build deploy clean logs stop

help:
	@echo "Available commands:"
	@echo "  install    - Install Python dependencies"
	@echo "  run        - Run the application locally"
	@echo "  test       - Run tests"
	@echo "  build      - Build Docker containers"
	@echo "  deploy     - Deploy with Docker Compose"
	@echo "  logs       - View application logs"
	@echo "  stop       - Stop Docker containers"
	@echo "  clean      - Clean up Docker containers and images"

install:
	pip install -r requirements.txt

run:
	cd E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system- && python app.py

test:
	python -m pytest test_app.py -v

build:
	docker-compose build

deploy:
	docker-compose up -d

logs:
	docker-compose logs -f

stop:
	docker-compose down

clean:
	docker-compose down --rmi all --volumes --remove-orphans
	docker system prune -f