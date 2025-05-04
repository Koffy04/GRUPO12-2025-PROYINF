from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

class Boletines(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    archivo_boletin = models.FileField(blank=True, null=True, upload_to='pdfs/')
    regiones = ArrayField(models.PositiveSmallIntegerField(), blank=True, null=True)
    etiqueta = ArrayField(models.CharField(max_length=30), blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    autor = models.CharField(max_length=200)
    fuente = models.CharField(max_length=50)
    image = models.ImageField(default='test.jpg')

    def str(self):
        return f'{self.nombre}'

    def set_regiones(self, regiones_list):
        self.regiones = regiones_list

#Enviar boletines a estos correos
class correos(models.Model):
    email = models.EmailField(primary_key=True)

class Perfil(models.Model):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Guarda el hash, no la contraseña en texto plano
    recibir_correos = models.BooleanField(default=False)
    
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        EDITOR = 'editor', 'Editor'
        LECTOR = 'lector', 'Lector'

    rol = models.CharField(max_length=10, choices=Roles.choices, default=Roles.LECTOR)

    def __str__(self):
        return self.email