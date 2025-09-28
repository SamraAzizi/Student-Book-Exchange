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