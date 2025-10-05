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