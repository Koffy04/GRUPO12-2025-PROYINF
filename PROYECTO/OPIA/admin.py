from django.contrib import admin
from .models import Boletines , correos, Perfil

admin.site.register(correos)
admin.site.register(Boletines)
admin.site.register(Perfil)