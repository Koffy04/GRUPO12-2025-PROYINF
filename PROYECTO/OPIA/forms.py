from django import forms
from .models import Perfil
from django.contrib.auth.hashers import make_password, check_password

class RegistroUsuario(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Perfil
        fields = ['nombre', 'email', 'password1', 'password2', 'recibir_correos']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Perfil.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Las contraseñas no coinciden.')

    def save(self, commit=True):
        perfil = super().save(commit=False)
        perfil.password = make_password(self.cleaned_data['password1'])
        if commit:
            perfil.save()
        return perfil



class LoginUsuario(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # Validar si el email existe en la base de datos
        try:
            perfil = Perfil.objects.get(email=email)
        except Perfil.DoesNotExist:
            raise forms.ValidationError("Usuario no encontrado.")

        # Verificar si la contraseña es correcta
        if not check_password(password, perfil.password):
            raise forms.ValidationError("Contraseña incorrecta.")
        
        # Si todo está correcto, devuelve el perfil (opcional)
        cleaned_data['perfil'] = perfil
        return cleaned_data
