# ================================
# COMPLETE PROJECT FILES
# ================================

# ================================
# 1. manage.py (ROOT DIRECTORY)
# ================================

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_exchange.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

# ================================
# 2. book_exchange/__init__.py
# ================================

# This file makes Python treat the directory as a package

# ================================
# 3. book_exchange/settings.py
# ================================

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-change-in-production-123456789'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.pythonanywhere.com', '.herokuapp.com', '.railway.app', '.render.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'marketplace',  # Our app
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
                'django.template.context_processors.media',  # For media files
            ],
        },
    },
]

WSGI_APPLICATION = 'book_exchange.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # For production

# Media files (User uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Message tags for Bootstrap compatibility
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# ================================
# 4. book_exchange/urls.py
# ================================

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('marketplace.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ================================
# 5. book_exchange/wsgi.py
# ================================

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_exchange.settings')

application = get_wsgi_application()

# ================================
# 6. marketplace/__init__.py
# ================================

# This file makes Python treat the directory as a package

# ================================
# 7. marketplace/apps.py
# ================================

from django.apps import AppConfig

class MarketplaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'marketplace'
    verbose_name = 'Student Marketplace'

# ================================
# 8. marketplace/models.py
# ================================

from django.db import models
from django.urls import reverse
from django.utils import timezone
from PIL import Image
import os

class Item(models.Model):
    ITEM_TYPES = [
        ('book', 'Textbook'),
        ('notes', 'Study Notes'),
    ]
    
    CONDITIONS = [
        ('excellent', 'Excellent - Like New'),
        ('good', 'Good - Minor Wear'),
        ('fair', 'Fair - Some Wear'),
        ('poor', 'Poor - Heavy Wear'),
    ]
    
    # Core fields as specified in requirements
    item_name = models.CharField(max_length=200, verbose_name="Item Name")
    description = models.TextField(verbose_name="Description", help_text="Describe the condition, highlights, missing pages, etc.")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price ($)")
    seller_name = models.CharField(max_length=100, verbose_name="Your Name")
    contact_info = models.CharField(max_length=200, verbose_name="Contact Info", help_text="WhatsApp number or email")
    image = models.ImageField(upload_to='item_images/', blank=True, null=True, verbose_name="Photo of Item")
    
    # Additional useful fields
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES, default='book', verbose_name="Type")
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name="Author/Creator")
    course = models.CharField(max_length=50, blank=True, null=True, verbose_name="Course Code", help_text="e.g., MATH 101, CS 201")
    condition = models.CharField(max_length=20, choices=CONDITIONS, default='good', verbose_name="Condition")
    date_posted = models.DateTimeField(default=timezone.now, verbose_name="Date Posted")
    is_sold = models.BooleanField(default=False, verbose_name="Sold")
    view_count = models.PositiveIntegerField(default=0, verbose_name="Views")
    
    class Meta:
        ordering = ['-date_posted']
        verbose_name = "Item"
        verbose_name_plural = "Items"
    
    def __str__(self):
        return self.item_name
    
    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Optimize uploaded images
        if self.image:
            img_path = self.image.path
            if os.path.exists(img_path):
                img = Image.open(img_path)
                # Convert to RGB if necessary
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                # Resize if too large
                if img.height > 800 or img.width > 800:
                    img.thumbnail((800, 800), Image.Resampling.LANCZOS)
                    img.save(img_path, optimize=True, quality=85)
    
    def increment_views(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    def get_contact_type(self):
        """Determine if contact is email or phone"""
        if '@' in self.contact_info:
            return 'email'
        else:
            return 'phone'

# ================================
# 9. marketplace/forms.py
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
            'item_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Calculus: Early Transcendentals',
                'required': True
            }),
            'item_type': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., James Stewart (optional)'
            }),
            'course': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., MATH 101 (optional)'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
                'required': True
            }),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe condition, any highlights, missing pages, etc.',
                'required': True
            }),
            'seller_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'required': True
            }),
            'contact_info': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'WhatsApp number or email address',
                'required': True
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price
    
    def clean_contact_info(self):
        contact = self.cleaned_data.get('contact_info')
        if contact:
            # Basic validation for email or phone
            if '@' not in contact and not any(char.isdigit() for char in contact):
                raise forms.ValidationError("Please enter a valid email address or phone number.")
        return contact

class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, author, course...'
        })
    )
    item_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Item.ITEM_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    course = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by course...'
        })
    )

# ================================
# 10. marketplace/views.py
# ================================

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Item
from .forms import ItemForm, SearchForm

def home(request):
    """Homepage showing latest items and statistics"""
    # Get latest items (not sold)
    latest_items = Item.objects.filter(is_sold=False).order_by('-date_posted')[:6]
    
    # Calculate statistics
    stats = {
        'total_items': Item.objects.filter(is_sold=False).count(),
        'total_books': Item.objects.filter(is_sold=False, item_type='book').count(),
        'total_notes': Item.objects.filter(is_sold=False, item_type='notes').count(),
        'total_sellers': Item.objects.filter(is_sold=False).values('seller_name').distinct().count(),
    }
    
    # Popular courses
    popular_courses = Item.objects.filter(is_sold=False, course__isnull=False).exclude(course='').values('course').annotate(
        count=Count('course')
    ).order_by('-count')[:5]
    
    context = {
        'latest_items': latest_items,
        'stats': stats,
        'popular_courses': popular_courses,
    }
    return render(request, 'home.html', context)

def post_item(request):
    """Form to POST a new item for sale"""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            messages.success(
                request, 
                f'🎉 Your "{item.item_name}" has been posted successfully! '
                f'Students can now contact you at {item.contact_info}'
            )
            return redirect('item_detail', pk=item.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ItemForm()
    
    return render(request, 'post_item.html', {'form': form})

def all_items(request):
    """GET and view all items with filtering and search"""
    items = Item.objects.filter(is_sold=False)
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        items = items.filter(
            Q(item_name__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(course__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(seller_name__icontains=search_query)
        )
    
    # Filter by type
    item_type = request.GET.get('type', '').strip()
    if item_type in ['book', 'notes']:
        items = items.filter(item_type=item_type)
    
    # Filter by course
    course_filter = request.GET.get('course', '').strip()
    if course_filter:
        items = items.filter(course__icontains=course_filter)
    
    # Filter by condition
    condition_filter = request.GET.get('condition', '').strip()
    if condition_filter:
        items = items.filter(condition=condition_filter)
    
    # Sort options
    sort_by = request.GET.get('sort', '-date_posted')
    valid_sorts = ['-date_posted', 'price', '-price', 'item_name', '-view_count']
    if sort_by in valid_sorts:
        items = items.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(items, 12)  # Show 12 items per page
    page_number = request.GET.get('page')
    items_page = paginator.get_page(page_number)
    
    # Get filter options
    all_courses = Item.objects.filter(
        is_sold=False, 
        course__isnull=False
    ).exclude(course='').values_list('course', flat=True).distinct().order_by('course')
    
    context = {
        'items': items_page,
        'total_results': items.count(),
        'search_query': search_query,
        'current_type': item_type,
        'current_course': course_filter,
        'current_condition': condition_filter,
        'current_sort': sort_by,
        'all_courses': all_courses,
        'conditions': Item.CONDITIONS,
    }
    return render(request, 'all_items.html', context)

def item_detail(request, pk):
    """Details page for each item"""
    item = get_object_or_404(Item, pk=pk)
    
    # Increment view count
    item.increment_views()
    
    # Handle mark as sold (simple version)
    if request.method == 'POST' and 'mark_sold' in request.POST:
        item.is_sold = True
        item.save()
        messages.success(request, f'"{item.item_name}" has been marked as sold!')
        return redirect('home')
    
    # Get related items (same course or type, excluding current item)
    related_items = Item.objects.filter(
        Q(course=item.course, course__isnull=False) | Q(item_type=item.item_type)
    ).exclude(pk=item.pk).filter(is_sold=False)[:3]
    
    # Get seller's other items
    other_items = Item.objects.filter(
        seller_name=item.seller_name,
        is_sold=False
    ).exclude(pk=item.pk)[:3]
    
    context = {
        'item': item,
        'related_items': related_items,
        'other_items': other_items,
    }
    return render(request, 'item_detail.html', context)

def search_ajax(request):
    """AJAX search for autocomplete"""
    query = request.GET.get('q', '').strip()
    if len(query) >= 2:
        items = Item.objects.filter(
            Q(item_name__icontains=query) |
            Q(course__icontains=query) |
            Q(author__icontains=query),
            is_sold=False
        )[:10]
        
        results = []
        for item in items:
            results.append({
                'id': item.pk,
                'name': item.item_name,
                'course': item.course or '',
                'price': str(item.price),
                'url': item.get_absolute_url()
            })
        return JsonResponse({'results': results})
    
    return JsonResponse({'results': []})

# ================================
# 11. marketplace/urls.py
# ================================

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/', views.post_item, name='post_item'),
    path('items/', views.all_items, name='all_items'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('search-ajax/', views.search_ajax, name='search_ajax'),
]

# ================================
# 12. marketplace/admin.py
# ================================

from django.contrib import admin
from django.utils.html import format_html
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'item_name', 'item_type', 'price', 'condition',
        'seller_name', 'course', 'date_posted', 'is_sold', 'view_count'
    ]
    list_filter = [
        'item_type', 'condition', 'is_sold', 'date_posted'
    ]
    search_fields = [
        'item_name', 'author', 'course', 'seller_name', 'description'
    ]
    list_editable = ['is_sold']
    readonly_fields = ['date_posted', 'view_count']
    date_hierarchy = 'date_posted'
    ordering = ['-date_posted']
    
    fieldsets = (
        ('Item Information', {
            'fields': ('item_name', 'item_type', 'author', 'course', 'condition', 'price', 'description', 'image')
        }),
        ('Seller Information', {
            'fields': ('seller_name', 'contact_info')
        }),
        ('Status', {
            'fields': ('is_sold', 'date_posted', 'view_count'),
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()
    
    actions = ['mark_as_sold', 'mark_as_available']
    
    def mark_as_sold(self, request, queryset):
        updated = queryset.update(is_sold=True)
        self.message_user(request, f'{updated} items marked as sold.')
    mark_as_sold.short_description = "Mark selected items as sold"
    
    def mark_as_available(self, request, queryset):
        updated = queryset.update(is_sold=False)
        self.message_user(request, f'{updated} items marked as available.')
    mark_as_available.short_description = "Mark selected items as available"

# Customize admin site
admin.site.site_header = "UniExchange Admin"
admin.site.site_title = "UniExchange Admin Portal"
admin.site.index_title = "Welcome to UniExchange Administration"

print("✅ ALL DJANGO FILES CREATED SUCCESSFULLY!")
print("🚀 Your complete Student Marketplace is ready to run!")
