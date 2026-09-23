from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Perfil


@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    """Cria um perfil de usuário quando um novo User é criado"""
    if created:
        Perfil.objects.get_or_create(usuario=instance)


@receiver(post_save, sender=User)
def salvar_perfil_usuario(sender, instance, **kwargs):
    """Salva o perfil do usuário quando o User é salvo"""
    if hasattr(instance, 'perfil'):
        instance.perfil.save()
