from django.shortcuts import render, redirect
from .models import Boletines

def boletines(request):
    boletines = Boletines.objects.all()  # Recupera todos los registros del modelo Boletines
    return render(request, 'pagina/boletines.html', {'boletines': boletines})

def inicio(request):
    return render(request, 'pagina/inicio.html')
