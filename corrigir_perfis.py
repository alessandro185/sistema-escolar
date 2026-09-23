"""
Script para corrigir perfis de usuários
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.usuarios.models import Perfil

print("=" * 50)
print("Corrigindo Perfis de Usuários")
print("=" * 50)

# Corrige admin -> diretor
admin_user = User.objects.filter(username='admin').first()
if admin_user:
    perfil, created = Perfil.objects.get_or_create(usuario=admin_user)
    perfil.cargo = 'diretora'
    perfil.save()
    print(f"  admin -> corrigido para 'diretora'")

# Corrige admin_esc -> administrativo
admin_esc = User.objects.filter(username='admin_esc').first()
if admin_esc:
    perfil, created = Perfil.objects.get_or_create(usuario=admin_esc)
    perfil.cargo = 'administrativo'
    perfil.save()
    print(f"  admin_esc -> corrigido para 'administrativo'")

# Corrige professores (professor2 a professor28)
from apps.professores.models import Professor
professores = User.objects.filter(username__startswith='professor')
for prof in professores:
    perfil, created = Perfil.objects.get_or_create(usuario=prof)
    if not perfil.cargo or perfil.cargo == '':
        perfil.cargo = 'professor'
        perfil.save()
        print(f"  {prof.username} -> corrigido para 'professor'")

print("\n" + "=" * 50)
print("Verificação final:")
print("=" * 50)

for u in User.objects.all():
    perfil = Perfil.objects.filter(usuario=u).first()
    if perfil:
        print(f"  {u.username:20} -> cargo: '{perfil.cargo}'")
    else:
        print(f"  {u.username:20} -> SEM PERFIL")