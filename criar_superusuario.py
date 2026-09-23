
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Criar superusuário padrão
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='diretora@escola.com',
        password='admin123',
        first_name='Ana',
        last_name='Beatriz'
    )
    print("Superusuário criado com sucesso!")
    print("Username: admin")
    print("Senha: admin123")
else:
    print("Superusuário já existe!")
