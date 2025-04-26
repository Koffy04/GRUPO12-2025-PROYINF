from django.urls import path
from . import views
from .views import boletines

urlpatterns = [
    path('boletines/', boletines, name='boletines'),
    path('', views.inicio, name='inicio'),
    path('buscar/', views.buscar_boletin, name='buscar_boletin'),
    path('enviar_correo/', views.enviar_correo, name='enviar_correo') 
]
