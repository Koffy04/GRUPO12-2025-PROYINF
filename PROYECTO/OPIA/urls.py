from django.urls import path
from . import views
from .views import logout_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('boletines/', views.boletines, name='boletines'),
    path('', views.inicio, name='inicio'),
    path('buscar/', views.buscar_boletin, name='buscar_boletin'),
    path('activar_notificaciones/', views.activar_notificaciones, name='activar_notificaciones'),
    path('elimminarc/', views.eliminarc, name='elimminarc'),
    path('privacidad/', views.privacidad, name='privacidad'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('registro/', views.registro, name='registro' ),
    path('logout/', logout_view, name='logout'),
    path('terminosycondiciones/', views.terminosycondiciones, name='terminosycondiciones')
]
