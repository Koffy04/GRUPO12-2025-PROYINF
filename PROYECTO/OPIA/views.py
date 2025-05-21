from django.shortcuts import render, redirect
from .models import Boletines, correos
from django.contrib.auth import logout
from django.db import IntegrityError
from .forms import RegistroUsuario
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
import requests
from django.http import HttpResponse
from django.views import View
import json

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

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuario(request.POST)
        if form.is_valid():
            usuario = form.save()
            return redirect('login')  # redirigí a donde quieras
    else:
        form = RegistroUsuario()
    return render(request, 'registro.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('inicio')

def eliminarc(request):
    return redirect('eliminarc')

def privacidad(request):
    return redirect('privacidad')

def terminosycondiciones(request):
    return redirect('terminosycondiciones')

class boletinDetailView(DetailView):
    model = Boletines
    template_name = 'boletin.html'
    context_object_name = 'boletin'
    
class ConvertPdfToWordView(View):
    def get(self, request, pk):
        boletin = get_object_or_404(Boletines, pk=pk)
        pdf_path = boletin.archivo_boletin.path  # ruta absoluta del PDF

        convertapi_secret = 'secret_gAEU1GJ4UbFZUgNS'

        with open(pdf_path, 'rb') as pdf_file:
            files = {'File': pdf_file}
            response = requests.post(
                f'https://v2.convertapi.com/pdf/to/docx?Secret={convertapi_secret}&StoreFile=true',
                files=files
            )

        try:
            result = response.json()
        except Exception:
            return HttpResponse("La respuesta no fue JSON. Error crudo: " + response.text, status=500)

        # Muestra el resultado completo como texto para depuración

        if response.status_code == 200:

            if 'Files' in result and result['Files'] and 'Url' in result['Files'][0]:
                file_url = result['Files'][0]['Url']
                word_file = requests.get(file_url)
                return HttpResponse(
                    word_file.content,
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    headers={'Content-Disposition': f'attachment; filename="{boletin.nombre}.docx"'}
                )
            else:
                error_message = result.get('Message', 'Error desconocido en la conversión.')
                return HttpResponse(f"Error en la conversión: {error_message}", status=500)
        else:
            return HttpResponse(f"Error en la conversión: {result}", status=500)