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