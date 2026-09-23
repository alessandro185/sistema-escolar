from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.usuarios.models import Perfil


class Command(BaseCommand):
    help = 'Cria usuários de teste para o sistema'
    
    def handle(self, *args, **options):
        test_users = [
            {
                'username': 'admin',
                'email': 'admin@escola.com.br',
                'first_name': 'Administrador',
                'last_name': 'Sistema',
                'password': 'admin123',
                'is_staff': True,
                'is_superuser': False,
                'cargo': 'diretor',
            },
            {
                'username': 'prof1',
                'email': 'prof1@escola.com.br',
                'first_name': 'João',
                'last_name': 'Professor',
                'password': 'prof123',
                'is_staff': False,
                'is_superuser': False,
                'cargo': 'professor',
            },
            {
                'username': 'prof2',
                'email': 'prof2@escola.com.br',
                'first_name': 'Maria',
                'last_name': 'Professor',
                'password': 'prof123',
                'is_staff': False,
                'is_superuser': False,
                'cargo': 'professor',
            },
            {
                'username': 'admin_esc',
                'email': 'admin@escola.com.br',
                'first_name': 'Administrativo',
                'last_name': 'Escola',
                'password': 'admin123',
                'is_staff': False,
                'is_superuser': False,
                'cargo': 'administrativo',
            },
        ]
        
        for user_data in test_users:
            cargo = user_data.pop('cargo')
            username = user_data['username']
            
            # Verificar se usuário já existe
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'Usuário {username} já existe. Pulando...')
                )
                continue
            
            # Criar usuário
            user = User.objects.create_user(**user_data)
            
            # Criar perfil
            perfil, created = Perfil.objects.get_or_create(usuario=user)
            perfil.cargo = cargo
            perfil.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Usuário {username} ({cargo}) criado com sucesso!'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS('✅ Todos os usuários de teste foram criados!')
        )
