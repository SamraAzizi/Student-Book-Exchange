# 📚 UniExchange - Student Book & Notes Marketplace

A web-based marketplace platform designed specifically for university students to buy and sell textbooks and study notes. Save money on expensive textbooks by purchasing from fellow students!

![Django](https://img.shields.io/badge/Django-4.2.7-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Problem It Solves

- **Expensive Textbooks**: University textbooks cost hundreds of dollars
- **Finding Good Notes**: Hard to find quality study materials from previous students
- **Campus Community**: No centralized platform for student-to-student trading
- **Sustainability**: Reuse books instead of buying new ones every semester

## ✨ Features

### Core Functionality
- 📖 **Browse Items**: View all available books and notes with detailed information
- 🔍 **Smart Search**: Filter by course, type, condition, and search keywords
- 📤 **Post Items**: Easy form to list books/notes for sale with image upload
- 💬 **Contact Sellers**: Direct email or WhatsApp integration
- 📱 **Mobile Responsive**: Works perfectly on phones, tablets, and desktops
- 🖼️ **Image Upload**: Upload photos of items for better visibility

### Additional Features
- 📊 **Statistics Dashboard**: View total books, notes, and active sellers
- 🎨 **Modern UI**: Clean, professional design with smooth animations
- 🔐 **Admin Panel**: Django admin interface for managing items
- 👁️ **View Counter**: Track how many people viewed each item
- 🔗 **Related Items**: Automatic suggestions for similar items
- 📄 **Pagination**: Easy navigation through large catalogs

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 4.2.7
- **Database**: SQLite3 (file-based, no server needed)
- **Language**: Python 3.8+
- **Image Processing**: Pillow 10.0.1

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Custom styling with animations
- **Bootstrap 5**: Responsive framework
- **JavaScript**: Interactive features

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone or Download Project
```bash
# Clone repository (if using Git)
git clone <repository-url>
cd UniExchange

# Or download and extract ZIP file
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Database
```bash
# Create database tables
python manage.py makemigrations marketplace
python manage.py migrate

# Create admin superuser (optional)
python manage.py createsuperuser
```

### Step 5: Run Development Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

