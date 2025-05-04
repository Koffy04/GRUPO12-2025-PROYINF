from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import perfil

class RegistroUsuario(UserCreationForm):
    class Meta:
        model = perfil
        fields = ['username','nombre', 'email', 'password1', 'password2', 'recibir_correos']

class LoginUsuario(AuthenticationForm):
    username = forms.EmailField(label='Email')
