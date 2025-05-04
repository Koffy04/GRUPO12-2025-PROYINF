from django.urls import path
from . import views

urlpatterns = [
    path('boletines/', views.boletines, name='boletines'),
    path('', views.inicio, name='inicio'),
    path('buscar/', views.buscar_boletin, name='buscar_boletin'),
    path('activar_notificaciones/', views.activar_notificaciones, name='activar_notificaciones'),
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
