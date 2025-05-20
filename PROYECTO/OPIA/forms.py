from django import forms
from .models import Perfil
from django.contrib.auth.forms import UserCreationForm

class RegistroUsuario(UserCreationForm):
    class Meta:
        model = Perfil
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'recibir_correos']

    def __init__(self, *args, **kwargs):
        super(RegistroUsuario, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Nombre de usuario'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Correo electrónico'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Nombre'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Apellido'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmar contraseña'})
        
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
