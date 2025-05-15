from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
import unittest
from unittest.mock import patch, MagicMock

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

class TestUbicacionAPI(unittest.TestCase):
    @patch('requests.get')  # Simula la función requests.get
    def test_get_city_success(self, mock_get):
        # Simula una respuesta exitosa de la API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "address": {
                "state": "Región Metropolitana de Santiago"
            }
        }
        mock_get.return_value = mock_response

        # Simula las coordenadas
        lat, lng = "-33.4489", "-70.6693"
        api_url = f"https://us1.locationiq.com/v1/reverse.php?key=pk.a73d396d2124f81921446f0ee1a967b5&lat={lat}&lon={lng}&format=json"

        # Llama a la API simulada
        response = mock_get(api_url)
        data = response.json()

        # Verifica que la API se haya llamado correctamente
        mock_get.assert_called_once_with(api_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("state", data["address"])
        self.assertEqual(data["address"]["state"], "Región Metropolitana de Santiago")

    @patch('requests.get')
    def test_get_city_failure(self, mock_get):
        # Simula una respuesta fallida de la API
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "Not Found"}
        mock_get.return_value = mock_response

        # Simula las coordenadas
        lat, lng = "-33.4489", "-70.6693"
        api_url = f"https://us1.locationiq.com/v1/reverse.php?key=pk.a73d396d2124f81921446f0ee1a967b5&lat={lat}&lon={lng}&format=json"

        # Llama a la API simulada
        response = mock_get(api_url)

        # Verifica que la API se haya llamado correctamente
        mock_get.assert_called_once_with(api_url)
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Not Found")

if __name__ == '__main__':
    unittest.main()