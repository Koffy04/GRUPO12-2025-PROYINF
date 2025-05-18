from django import forms
from .models import Perfil
from django.contrib.auth.forms import UserCreationForm

class RegistroUsuario(UserCreationForm):
    class Meta:
        model = Perfil
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'recibir_correos']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Perfil.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email

    def save(self, commit=True):
        perfil = super().save(commit=False)
        perfil.set_password(self.cleaned_data['password1'])  # Ya se maneja bien
        if commit:
            perfil.save()
        return perfil
