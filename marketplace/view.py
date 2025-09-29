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