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