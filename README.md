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

## 🚀 Usage

### For Students Selling Items

1. Click **"Sell Item"** in navigation
2. Fill out the form:
   - Item name and type (book/notes)
   - Author and course code
   - Price and condition
   - Description
   - Your contact info (email or WhatsApp)
   - Upload a photo (optional)
3. Submit and share your listing!

### For Students Buying Items

1. Browse the homepage or click **"Browse All"**
2. Use filters to find:
   - Specific courses
   - Books or notes
   - Price range
3. Click on items for full details
4. Contact seller via email or WhatsApp
5. Arrange campus meetup for exchange

### Admin Access

1. Go to: **http://127.0.0.1:8000/admin/**
2. Login with superuser credentials
3. Manage items, mark as sold, view statistics

## 📁 Project Structure

```
UniExchange/
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── db.sqlite3                # SQLite database (after migration)
│
├── book_exchange/            # Main project folder
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py               # WSGI configuration
│
├── marketplace/              # Main app folder
│   ├── models.py             # Database models (Item)
│   ├── views.py              # View functions
│   ├── urls.py               # App URL patterns
│   ├── forms.py              # Form definitions
│   ├── admin.py              # Admin panel configuration
│   └── migrations/           # Database migrations
│
├── templates/                # HTML templates
│   ├── base.html             # Base template
│   ├── home.html             # Homepage
│   ├── post_item.html        # Post new item form
│   ├── all_items.html        # Browse all items
│   └── item_detail.html      # Item detail page
│
├── static/                   # Static files
│   └── css/
│       └── style.css         # Custom CSS
│
└── media/                    # User uploaded files
    └── item_images/          # Item photos
```



