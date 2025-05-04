from .models import Perfil

def perfil_autenticado(request):
    perfil = None
    perfil_id = request.session.get('perfil_id')
    if perfil_id:
        try:
            perfil = Perfil.objects.get(id=perfil_id)
        except Perfil.DoesNotExist:
            pass
    return {'perfil': perfil}
