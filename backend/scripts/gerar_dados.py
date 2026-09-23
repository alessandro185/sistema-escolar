
import os
import django
import random
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.alunos.models import Aluno
from apps.turmas.models import Turma
from apps.professores.models import Professor
from apps.funcionarios.models import Funcionario

# Limpar dados existentes
print("Limpando dados existentes...")
Aluno.objects.all().delete()
Professor.objects.all().delete()
User.objects.filter(is_superuser=False).delete()
Funcionario.objects.all().delete()

# Nomes para gerar dados
nomes_masculinos = [
    "Joao Silva", "Pedro Santos", "Carlos Oliveira", "Lucas Souza", "Mateus Costa", 
    "Andre Pereira", "Gabriel Almeida", "Rafael Fernandes", "Bruno Lima", "Guilherme Carvalho",
    "Leonardo Araujo", "Daniel Rocha", "Eduardo Ribeiro", "Murilo Goncalves", "Felipe Martins",
    "Gustavo Cardoso", "Vinicius Soares", "Luan Ferreira", "Matheus Mendes", "Pablo Nascimento",
    "Caio Azevedo", "Thiago Barbosa", "Igor Viana", "Ricardo Cunha", "Alexandre Pires",
    "Diego Sousa", "Caue Monteiro", "Enzo Gomes", "Julio Macedo", "Vitor Nogueira"
]

nomes_femininos = [
    "Maria Souza", "Ana Oliveira", "Francisca Silva", "Adriana Costa", "Juliana Santos",
    "Mariana Pereira", "Fernanda Almeida", "Patricia Fernandes", "Aline Lima", "Camila Carvalho",
    "Amanda Araujo", "Bruna Rocha", "Carla Ribeiro", "Daniela Goncalves", "Eduarda Martins",
    "Gabriela Cardoso", "Isabela Soares", "Jessica Ferreira", "Leticia Mendes", "Luiza Nascimento",
    "Manuela Azevedo", "Marina Barbosa", "Natalia Viana", "Nicole Cunha", "Priscila Pires",
    "Rafaela Sousa", "Sabrina Monteiro", "Sofia Gomes", "Tatiane Macedo", "Vanessa Nogueira"
]

sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Costa", "Pereira", "Almeida", "Fernandes", "Lima", "Carvalho"]

disciplinas_professores = [
    "Matematica", "Portugues", "Historia", "Geografia", "Fisica", "Quimica", 
    "Biologia", "Educacao Fisica", "Artes", "Ingles", "Filosofia", "Sociologia"
]

departamentos_funcionarios = ["exatas", "humanas", "artes", "pedagogico", "administrativo"]

# Obter todas as turmas
turmas = list(Turma.objects.all())
print(f"Turmas disponiveis: {len(turmas)}")

# Gerar 480 alunos (40 por turma)
print("\nGerando 480 alunos...")
alunos_criados = 0
for turma in turmas:
    for i in range(40):
        # Escolher nome aleatorio
        if random.choice([True, False]):
            nome = random.choice(nomes_masculinos)
        else:
            nome = random.choice(nomes_femininos)
        
        # Gerar matricula
        matricula = f"2024{turma.ano}{turma.letra}{i+1:02d}"
        
        # Gerar data de nascimento (14-18 anos)
        hoje = datetime.now()
        idade = random.randint(14, 18)
        data_nascimento = hoje - timedelta(days=idade*365 + random.randint(0, 365))
        
        # Gerar CPF (fake)
        cpf = f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}"
        
        # Gerar telefone
        telefone = f"({random.randint(80,99)}) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}"
        
        # Criar aluno
        aluno = Aluno.objects.create(
            matricula=matricula,
            nome=nome,
            data_nascimento=data_nascimento.date(),
            cpf=cpf,
            genero=random.choice(["M", "F"]),
            telefone=telefone,
            turma=turma,
            ativo=True,
            responsavel_nome=f"{random.choice(nomes_masculinos) if random.choice([True,False]) else random.choice(nomes_femininos)}",
            responsavel_telefone=telefone,
            endereco=f"Rua {random.choice(sobrenomes)}",
            numero=f"{random.randint(10,999)}",
            bairro="Centro",
            cidade="Fortaleza",
            estado="CE"
        )
        alunos_criados += 1
        if alunos_criados % 100 == 0:
            print(f"  Criados {alunos_criados} alunos...")

print(f"{alunos_criados} alunos criados com sucesso!")

# Gerar 28 professores
print("\nGerando 28 professores...")
professores_criados = 0
for i in range(28):
    # Nome
    if random.choice([True, False]):
        nome = random.choice(nomes_masculinos)
    else:
        nome = random.choice(nomes_femininos)
    
    # Criar usuario
    username = f"professor{i+1}"
    first_name = nome.split()[0]
    last_name = " ".join(nome.split()[1:])
    usuario = User.objects.create_user(
        username=username,
        email=f"{username}@escola.com",
        cargo="professor",
        password="professor123",
        first_name=first_name,
        last_name=last_name
    )
    
    # Criar professor
    professor = Professor.objects.create(
        usuario=usuario,
        disciplina=random.choice(disciplinas_professores),
        carga_horaria=random.choice([20, 30, 40]),
        ativo=True
    )
    
    # Associar a turmas aleatorias
    turmas_professor = random.sample(turmas, random.randint(2, 4))
    professor.turmas.add(*turmas_professor)
    
    professores_criados += 1

print(f"{professores_criados} professores criados com sucesso!")

# Gerar 14 funcionarios administrativos
print("\nGerando 14 funcionarios...")
funcionarios_criados = 0

# Primeiro, a diretora (Ana Beatriz)
Funcionario.objects.create(
    id_func="FUNC-728",
    nome="Ana Beatriz",
    cargo="diretor",
    departamento="pedagogico",
    carga_horaria=40,
    salario_base=8000.00,
    data_admissao=datetime(2020, 1, 15).date(),
    ativo=True
)
funcionarios_criados += 1

# Gerar os outros 13
for i in range(13):
    if random.choice([True, False]):
        nome = random.choice(nomes_masculinos)
    else:
        nome = random.choice(nomes_femininos)
    
    # ID Funcional
    id_func = f"FUNC-{random.randint(100, 999)}"
    
    # Cargo (administrativo ou outro, menos diretor)
    cargo = random.choice(["administrativo", "coordenador", "outro"])
    
    # Departamento
    departamento = random.choice(departamentos_funcionarios)
    
    # Salario
    if cargo == "coordenador":
        salario = random.randint(5000, 7000)
    elif cargo == "administrativo":
        salario = random.randint(2500, 4000)
    else:
        salario = random.randint(2000, 3500)
    
    # Data de admissao
    ano_admissao = random.randint(2015, 2024)
    mes_admissao = random.randint(1, 12)
    dia_admissao = random.randint(1, 28)
    data_admissao = datetime(ano_admissao, mes_admissao, dia_admissao).date()
    
    Funcionario.objects.create(
        id_func=id_func,
        nome=nome,
        cargo=cargo,
        departamento=departamento,
        carga_horaria=random.choice([40, 44]),
        salario_base=salario,
        data_admissao=data_admissao,
        ativo=True
    )
    funcionarios_criados += 1

print(f"{funcionarios_criados} funcionarios criados com sucesso!")

# Verificar contagens finais
print("\n=== CONTAGENS FINAIS ===")
print(f"Alunos: {Aluno.objects.filter(ativo=True).count()}")
print(f"Professores: {Professor.objects.filter(ativo=True).count()}")
print(f"Funcionarios: {Funcionario.objects.filter(ativo=True).count()}")
print(f"Turmas: {Turma.objects.filter(ativa=True).count()}")

print("\nDados gerados com sucesso!")
