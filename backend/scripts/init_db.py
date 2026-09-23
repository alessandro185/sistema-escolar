"""
Script para inicializar o banco de dados com dados de teste
Execute com: python backend/manage.py shell < backend/scripts/init_db.py
"""

import os
import django
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group
from apps.usuarios.models import Perfil
from apps.turmas.models import Turma
from apps.professores.models import Professor
from apps.alunos.models import Aluno
from datetime import date, timedelta
import random

def criar_grupos():
    """Criar grupos de permissão"""
    print("Criando grupos...")
    Group.objects.get_or_create(name='Diretor')
    Group.objects.get_or_create(name='Professor')
    Group.objects.get_or_create(name='Administrativo')
    print("[OK] Grupos criados")

def criar_usuarios():
    """Criar usuários de teste"""
    print("\nCriando usuários...")
    
    usuarios_data = [
        {'username': 'admin', 'password': 'admin123', 'first_name': 'Administrador', 'cargo': 'diretor'},
        {'username': 'professor1', 'password': 'professor123', 'first_name': 'Carlos', 'last_name': 'Silva', 'cargo': 'professor'},
        {'username': 'professor2', 'password': 'professor123', 'first_name': 'Maria', 'last_name': 'Santos', 'cargo': 'professor'},
        {'username': 'admin_esc', 'password': 'admin123', 'first_name': 'Secretária', 'cargo': 'administrativo'},
    ]
    
    usuarios_criados = []
    for u_data in usuarios_data:
        username = u_data['username']
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                password=u_data['password'],
                first_name=u_data.get('first_name', ''),
                last_name=u_data.get('last_name', ''),
                email=f"{username}@escola.com"
            )
            
            # Criar perfil
            cargo = u_data['cargo']
            perfil, _ = Perfil.objects.get_or_create(usuario=user, defaults={'cargo': cargo})
            
            # Criar Professor se for professor
            if cargo == 'professor':
                Professor.objects.get_or_create(
                    usuario=user,
                    defaults={'disciplina': 'Matemática' if random.random() > 0.5 else 'Português', 'carga_horaria': 20}
                )
            
            usuarios_criados.append(user)
            print(f"  [OK] Usuario {username} criado")
        else:
            print(f"  ! Usuário {username} já existe")
    
    return usuarios_criados

def criar_turmas():
    """Criar turmas"""
    print("\nCriando turmas...")
    
    turmas_data = [
        (1, 'A'), (1, 'B'), (1, 'C'), (1, 'D'),
        (2, 'A'), (2, 'B'), (2, 'C'), (2, 'D'),
        (3, 'A'), (3, 'B'), (3, 'C'), (3, 'D'),
    ]
    
    turmas = []
    for ano, letra in turmas_data:
        turma, created = Turma.objects.get_or_create(
            ano=ano,
            letra=letra,
            ano_letivo=2024,
            defaults={'ativa': True}
        )
        if created:
            print(f"  [OK] Turma {ano} - {letra} criada")
            turmas.append(turma)
        else:
            turmas.append(turma)
    
    return turmas

def criar_alunos(turmas):
    """Criar alunos de teste"""
    print("\nCriando alunos...")
    
    nomes = [
        'Joao Silva', 'Maria Santos', 'Carlos Oliveira', 'Ana Costa',
        'Pedro Alves', 'Lucia Ferreira', 'Antonio Martins', 'Juliana Sousa',
        'Felipe Rosa', 'Beatriz Rocha', 'Lucas Dias', 'Sofia Barros',
    ]
    
    total_alunos_criados = 0
    contador = 0
    for turma in turmas:
        # 40 alunos por turma
        for i in range(40):
            contador += 1
            nome = random.choice(nomes)
            cpf = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"
            matricula = f"MAT{2024}{turma.ano}{turma.letra}{contador:04d}"
            
            try:
                aluno = Aluno.objects.create(
                    nome=f"{nome} {contador}",
                    cpf=cpf,
                    data_nascimento=date(2005, random.randint(1, 12), random.randint(1, 28)),
                    genero=random.choice(['M', 'F']),
                    email=f"aluno{contador}@escola.com",
                    turma=turma,
                    matricula=matricula,
                    ativo=True,
                    endereco="Rua Teste",
                    numero="123",
                    bairro="Bairro",
                    cidade="Cidade",
                    estado="SP",
                    cep="12345-678"
                )
                total_alunos_criados += 1
                if contador % 100 == 0:
                    print(f"    {contador} alunos criados...")
            except Exception as e:
                if contador <= 3:
                    print(f"    DEBUG: Erro ao criar aluno {contador}: {str(e)}")
    
    print(f"  [OK] {total_alunos_criados} alunos criados")

def main():
    print("=" * 50)
    print("Inicializando banco de dados...")
    print("=" * 50)
    
    criar_grupos()
    criar_usuarios()
    turmas = criar_turmas()
    criar_alunos(turmas)
    
    print("\n" + "=" * 50)
    print("[OK] Banco de dados inicializado com sucesso!")
    print("=" * 50)
    print("\nContas de teste:")
    print("  Diretor: admin / admin123")
    print("  Professor: professor1 / professor123")
    

if __name__ == '__main__':
    main()
