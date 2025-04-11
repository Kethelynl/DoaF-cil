from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .models import Profile, UserAddress
from django import forms

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    phone = PhoneNumberField(region="BR", required=True)
    group = forms.ChoiceField(choices=[('Doador', 'Doador'), ('Recebidor', 'Receber Doação')], required=True)
    

    class Meta:
        model = User
        fields = ['username', 'email', 'phone','password1', 'password2', 'group']

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField()
    phone = PhoneNumberField(region="BR", required=True)

    class Meta:
        model = User
        fields = ['email', 'phone']

class DesignProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Campos do formulário:", self.fields)  # Isso mostrará se "image" está presente

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['rua', 'numero', 'cidade', 'estado', 'codigo']