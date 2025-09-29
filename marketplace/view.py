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