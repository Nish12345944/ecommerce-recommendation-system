# Ecommerce RecSys - AI-Powered E-Commerce Platform

A modern e-commerce platform with AI-powered product recommendations built with React and Flask.

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Backend runs on: http://localhost:5000

### Frontend Setup
```bash
cd frontend
npm install
npm start
```
Frontend runs on: http://localhost:3000

## 📁 Project Structure
```
ecommerce-recsys/
├── backend/
│   ├── app.py              # Flask API server
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/         # Page components
│   │   ├── store/         # State management
│   │   └── utils/         # API utilities
│   └── package.json       # Node dependencies
└── README.md
```

## 🎯 Features
- Modern React frontend with Tailwind CSS
- Flask REST API backend
- Product catalog with search and filtering
- Shopping cart functionality
- AI-powered product recommendations
- Responsive design

## 🛠 Tech Stack
- **Frontend**: React, Tailwind CSS, Zustand, Framer Motion
- **Backend**: Flask, Flask-CORS
- **State Management**: Zustand with persistence
- **Styling**: Tailwind CSS with custom design system