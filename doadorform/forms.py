from django import forms
from .models import ProductD

class ProductDForm(forms.ModelForm):
    class Meta:
        model = ProductD
        fields = ['name', 'quantity', 'category', 'photo']