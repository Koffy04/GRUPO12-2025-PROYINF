from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Boletines, correos

@receiver(post_save, sender=Boletines)
def enviar_correos_boletin(sender, instance, created, **kwargs):
    if created:
        destinatarios = correos.objects.values_list('email', flat=True)

        asunto = f"Nuevo boletín: {instance.nombre}"
        mensaje = f"Se ha publicado un nuevo boletín.\nFuente: {instance.fuente}\nAutor: {instance.autor}"

        # Crear el mensaje de correo
        email = EmailMessage(
            subject=asunto,
            body=mensaje,
            from_email=settings.EMAIL_HOST_USER,
            to=destinatarios,
        )

        # Si hay archivo, adjuntarlo
        if instance.archivo_boletin:
            archivo_path = instance.archivo_boletin.path  # Ruta absoluta del archivo en el sistema

            try:
                with open(archivo_path, 'rb') as f:
                    email.attach(instance.archivo_boletin.name, f.read(), 'application/pdf')
            except Exception as e:
                print(f"No se pudo adjuntar el archivo: {e}")

        try:
            email.send(fail_silently=False)
            print("Correo enviado correctamente.")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")
