from django.urls import path
from . import views
from .views import boletines

urlpatterns = [
    path('boletines/', boletines, name='boletines'),
    path('', views.inicio, name='inicio'),
    path('buscar/', views.buscar_boletin, name='buscar_boletin'),
    path('activar_notificaciones/', views.activar_notificaciones, name='activar_notificaciones'),
    path('login/', views.iniciar_sesion, name='login'),
    path('registro/', views.registro, name='registro')
]
