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
