import unittest
import os
import django

from django.test import Client
from django.contrib.auth import get_user_model

# Configuración del entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROYECTO.settings')
django.setup()

class LoginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.User = get_user_model()
        cls.client = Client()
        cls.User = cls.User.objects.create_user(username='testuser', email='test@test.com', password='12345')

    def test_login_exitoso(self):
        client = Client()
        response = client.post('/accounts/login/', {
            'login': 'testuser',
            'password': '12345'
        }, follow=True)

        user_id = client.session.get('_auth_user_id')
        print("user_id en sesión (login exitoso):", user_id)

        self.assertIsNotNone(user_id, "El usuario no fue autenticado correctamente")
        self.assertEqual(int(user_id), self.user.id)

    def test_login_fallido(self):
        client = Client()
        response = client.post('/accounts/login/', {
            'login': 'testuser',
            'password': 'wrongpass'
        })

        user_id = client.session.get('_auth_user_id')
        print("user_id en sesión (login fallido):", user_id)

        self.assertIsNone(user_id, "El usuario **no** debería autenticarse con contraseña incorrecta")
    @classmethod
    def tearDownClass(cls):
        cls.User.objects.filter(username='testuser').delete()
        super().tearDownClass()