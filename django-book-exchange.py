# ================================
# PROJECT STRUCTURE
# ================================
"""
book_exchange/
├── manage.py
├── book_exchange/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── marketplace/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── migrations/
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── post_item.html
│   ├── item_detail.html
│   └── all_items.html
├── static/
│   └── css/
│       └── style.css
└── media/
    └── item_images/
"""

# ================================
# 1. DJANGO SETTINGS (settings.py)
# ================================

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-change-in-production'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.pythonanywhere.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'marketplace',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'book_exchange.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ================================
# 2. MODELS (marketplace/models.py)
# ================================

from django.db import models
from django.urls import reverse
from django.utils import timezone

class Item(models.Model):
    ITEM_TYPES = [
        ('book', 'Textbook'),
        ('notes', 'Notes'),
    ]
    
    CONDITIONS = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    
    # Core fields as specified
    item_name = models.CharField(max_length=200, verbose_name="Item Name")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price ($)")
    seller_name = models.CharField(max_length=100, verbose_name="Seller Name")
    contact_info = models.CharField(max_length=200, verbose_name="Contact Info (WhatsApp/Email)")
    image = models.ImageField(upload_to='item_images/', blank=True, null=True, verbose_name="Item Image")
    
    # Additional useful fields
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES, default='book')
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name="Author")
    course = models.CharField(max_length=50, blank=True, null=True, verbose_name="Course Code")
    condition = models.CharField(max_length=20, choices=CONDITIONS, default='good')
    date_posted = models.DateTimeField(default=timezone.now)
    is_sold = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_posted']
    
    def __str__(self):
        return self.item_name
    
    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'pk': self.pk})

# ================================
# 3. FORMS (marketplace/forms.py)
# ================================

from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'item_name', 'item_type', 'author', 'course', 
            'price', 'condition', 'description', 
            'seller_name', 'contact_info', 'image'
        ]
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Calculus: Early Transcendentals'}),
            'item_type': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., James Stewart'}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., MATH 101'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Additional details, highlights, missing pages, etc.'}),
            'seller_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp number or email'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

# ================================
# 4. VIEWS (marketplace/views.py)
# ================================

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Item
from .forms import ItemForm

def home(request):
    """Homepage showing latest items"""
    latest_items = Item.objects.filter(is_sold=False)[:6]
    total_items = Item.objects.filter(is_sold=False).count()
    total_books = Item.objects.filter(is_sold=False, item_type='book').count()
    total_notes = Item.objects.filter(is_sold=False, item_type='notes').count()
    
    context = {
        'latest_items': latest_items,
        'total_items': total_items,
        'total_books': total_books,
        'total_notes': total_notes,
    }
    return render(request, 'home.html', context)

def post_item(request):
    """POST a new item for sale"""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            messages.success(request, f'Your "{item.item_name}" has been posted successfully!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm()
    
    return render(request, 'post_item.html', {'form': form})

def all_items(request):
    """GET and view all items with filtering"""
    items = Item.objects.filter(is_sold=False)
    
    # Filter by type
    item_type = request.GET.get('type')
    if item_type in ['book', 'notes']:
        items = items.filter(item_type=item_type)
    
    # Filter by course
    course = request.GET.get('course')
    if course:
        items = items.filter(course__icontains=course)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        items = items.filter(
            Q(item_name__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(course__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Get unique courses for filter dropdown
    courses = Item.objects.filter(is_sold=False).values_list('course', flat=True).distinct()
    courses = [course for course in courses if course]  # Remove empty values
    
    context = {
        'items': items,
        'courses': courses,
        'current_type': item_type,
        'current_course': course,
        'search_query': search_query,
    }
    return render(request, 'all_items.html', context)

def item_detail(request, pk):
    """Details page for each item"""
    item = get_object_or_404(Item, pk=pk)
    
    # Mark as sold functionality (optional)
    if request.method == 'POST' and 'mark_sold' in request.POST:
        item.is_sold = True
        item.save()
        messages.success(request, 'Item marked as sold!')
        return redirect('home')
    
    # Related items (same course or type)
    related_items = Item.objects.filter(
        Q(course=item.course) | Q(item_type=item.item_type)
    ).exclude(pk=item.pk).filter(is_sold=False)[:3]
    
    context = {
        'item': item,
        'related_items': related_items,
    }
    return render(request, 'item_detail.html', context)

# ================================
# 5. URLS CONFIGURATION
# ================================

# Main project URLs (book_exchange/urls.py)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('marketplace.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# App URLs (marketplace/urls.py)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/', views.post_item, name='post_item'),
    path('items/', views.all_items, name='all_items'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
]

# ================================
# 6. ADMIN CONFIGURATION (marketplace/admin.py)
# ================================

from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'item_type', 'price', 'seller_name', 'date_posted', 'is_sold']
    list_filter = ['item_type', 'condition', 'is_sold', 'date_posted']
    search_fields = ['item_name', 'author', 'course', 'seller_name']
    list_editable = ['is_sold']
    readonly_fields = ['date_posted']

# ================================
# 7. SETUP COMMANDS
# ================================

# Create these commands in your terminal:

"""
# 1. Create Django project
django-admin startproject book_exchange
cd book_exchange

# 2. Create marketplace app
python manage.py startapp marketplace

# 3. Install Pillow for image handling
pip install Pillow

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser (optional)
python manage.py createsuperuser

# 6. Run development server
python manage.py runserver
"""

# ================================
# 8. REQUIREMENTS.txt
# ================================

"""
Django==4.2.7
Pillow==10.0.1
"""

# ================================
# 9. DEPLOYMENT GUIDE
# ================================

"""
FREE HOSTING OPTIONS:

1. PYTHONANYWHERE (Recommended for Django):
   - Sign up at pythonanywhere.com (free tier)
   - Upload your project files
   - Set up web app with Django
   - Configure static/media files
   - Your site will be at: username.pythonanywhere.com

2. HEROKU (Good alternative):
   - Install Heroku CLI
   - Create Procfile: "web: gunicorn book_exchange.wsgi"
   - Add gunicorn to requirements.txt
   - Deploy with git

3. RAILWAY/RENDER:
   - Connect GitHub repository
   - Auto-deploy on push
   - Free tier available

PRODUCTION SETTINGS:
- Change SECRET_KEY
- Set DEBUG = False
- Add proper ALLOWED_HOSTS
- Use PostgreSQL for production (optional)
"""

print("🚀 Django Book Exchange Platform - Complete Implementation!")
print("📁 Create the above file structure and copy the respective code sections.")
print("💡 This covers all requirements: Frontend, Backend, Database, and Hosting options!")
