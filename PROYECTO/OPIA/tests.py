import os
from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from unittest.mock import patch
from OPIA.models import Boletines  # Cambia "opia" si tu app tiene otro nombre

class ConvertPdfToWordViewTest(TestCase):

    def setUp(self):
        # Asegurar carpeta MEDIA_ROOT/boletines/
        self.media_dir = settings.MEDIA_ROOT
        os.makedirs(os.path.join(self.media_dir, 'boletines'), exist_ok=True)

        # Crear archivo PDF real
        self.pdf_filename = 'boletines/test.pdf'
        self.pdf_path = os.path.join(self.media_dir, self.pdf_filename)
        with open(self.pdf_path, 'wb') as f:
            f.write(b'%PDF-1.4 contenido de prueba')

        # Crear instancia real de Boletines
        self.boletin = Boletines.objects.create(
            nombre="BoletinTest",
            archivo_boletin=self.pdf_filename  # Django guarda ruta relativa
        )

    def tearDown(self):
        if os.path.exists(self.pdf_path):
            os.remove(self.pdf_path)

    @patch('OPIA.views.requests.post')
    @patch('OPIA.views.requests.get')
    def test_conversion_successful(self, mock_get, mock_post):
        # Simular respuesta exitosa de la API externa
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "Files": [
                {"Url": "https://fakeurl.com/archivo.docx"}
            ]
        }
        mock_get.return_value.content = b'Contenido Word Falso'

        response = self.client.get(f'/convertir/{self.boletin.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        self.assertIn(b'Contenido Word Falso', response.content)

    @patch('OPIA.views.requests.post')   
    def test_conversion_api_fails(self, mock_post):
        # Simular que la API devuelve un status code diferente de 200, sin JSON válido
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {"Message": "Bad request"}

        response = self.client.get(f'/convertir/{self.boletin.pk}/')

        self.assertEqual(response.status_code, 500)
        self.assertIn("Error en la conversión", response.content.decode())

