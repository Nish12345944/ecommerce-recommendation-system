@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Starting E-Commerce Recommendation System...
python run_app.py

pause