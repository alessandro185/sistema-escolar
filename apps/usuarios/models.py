from django.contrib.auth.models import User
from django.db import models


class Perfil(models.Model):
    """Perfil de usuário com cargo e permissões"""
    
    CARGO_CHOICES = [
        ('diretora', 'Diretora'),
        ('professor', 'Professor(a)'),
        ('administrativo', 'Administrativo'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    cargo = models.CharField(
        max_length=20,
        choices=CARGO_CHOICES,
        default='professor',
        verbose_name='Cargo'
    )
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} ({self.get_cargo_display_label()})"
    
    def get_cargo_display_label(self):
        """Retorna o label do cargo ou 'Usuário' se não encontrado."""
        return dict(self.CARGO_CHOICES).get(self.cargo, 'Usuário')
from django.db import models


# Modelo base para auditoria
class TimeStampedModel(models.Model):
    """Abstract base model com campos de timestamp"""
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        abstract = True
