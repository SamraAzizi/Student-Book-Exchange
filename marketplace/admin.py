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