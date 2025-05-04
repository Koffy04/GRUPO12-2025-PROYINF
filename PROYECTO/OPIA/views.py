from django.shortcuts import render, redirect
from .models import Boletines, correos, Perfil
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .forms import RegistroUsuario

def boletines(request):
    boletines = Boletines.objects.all().order_by('timestamp').reverse()
    etiquetas = Boletines.objects.values_list('etiqueta', flat=True)

    etiquetas_unicas = set()
    for lista_etiquetas in etiquetas:
        if lista_etiquetas:
            etiquetas_unicas.update(lista_etiquetas)

    etiquetas_unicas = sorted(etiquetas_unicas)
    return render(request, 'boletines.html', {'boletines': boletines, 'etiquetas_unicas': etiquetas_unicas})

def buscar_boletin(request):
    categoria = request.GET.get('filtro1', 'f1')
    region = request.GET.get('filtro2', 'f2')
    palabra_clave = request.GET.get('filtro3', '')

    boletines = Boletines.objects.all()
    if categoria != 'f1':  # Si se seleccionó una categoría específica
        boletines = boletines.filter(etiqueta__contains=[categoria])  # Filtrar con el array de etiquetas

    if region != 'f2':  # Verifica si el usuario seleccionó una región específica
        region = int(region)  # Convertir la región a entero
        boletines = boletines.filter(regiones__contains=[region])

    if palabra_clave:  # Si hay una palabra clave
        boletines = boletines.filter(nombre__icontains=palabra_clave)

    etiquetas = Boletines.objects.values_list('etiqueta', flat=True)
    etiquetas_unicas = set()
    for lista_etiquetas in etiquetas:
        if lista_etiquetas:  # Asegurarse de que la lista no esté vacía
            etiquetas_unicas.update(lista_etiquetas)

    etiquetas_unicas = sorted(etiquetas_unicas)

    return render(request, 'boletines.html', {'boletines': boletines , 'etiquetas_unicas': etiquetas_unicas})

def inicio(request):
    boletines = Boletines.objects.all().order_by('timestamp').reverse()
    etiquetas = Boletines.objects.values_list('etiqueta', flat=True)
    etiquetas_unicas = set()
    
    for lista_etiquetas in etiquetas:
        if lista_etiquetas:
            etiquetas_unicas.update(lista_etiquetas)

    etiquetas_unicas = sorted(etiquetas_unicas)
    return render(request, 'index.html',{'boletines': boletines, 'etiquetas_unicas': etiquetas_unicas})

def activar_notificaciones(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            correos.objects.create(email=email)
        except IntegrityError:
            pass  
    return render(request, 'boletines.html')

def registro_view(request):
    if request.method == 'POST':
        form = RegistroUsuario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')  
    else:
        form = RegistroUsuario()
    return render(request, 'registro.html', {'form': form})