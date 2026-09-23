"""
Script para verificar perfis de usuários
"""
import os
import django
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.usuarios.models import Perfil

print("=" * 50)
print("Verificação de Perfis de Usuários")
print("=" * 50)

users = User.objects.all()
print(f"\nTotal de usuários: {users.count()}")
print(f"Total de perfis: {Perfil.objects.count()}")

print("\nDetalhamento por usuário:")
for u in users:
    perfil = Perfil.objects.filter(usuario=u).first()
    if perfil:
        print(f"  {u.username:20} -> cargo: '{perfil.cargo}'")
    else:
        print(f"  {u.username:20} -> SEM PERFIL")
