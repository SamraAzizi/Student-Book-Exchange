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