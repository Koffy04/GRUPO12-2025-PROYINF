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