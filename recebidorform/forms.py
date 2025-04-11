from django import forms
from .models import PedidoForm

class PedidoForm(forms.ModelForm):
    class Meta:
        model = PedidoForm
        fields = ['name', 'quantity', 'category', 'photo']