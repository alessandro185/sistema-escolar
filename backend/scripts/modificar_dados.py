
import os
import django
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.alunos.models import Aluno
from random import sample


def main():
    # Pega todos os alunos
    alunos = list(Aluno.objects.all())
    
    # Limpa todos os emails primeiro
    for aluno in alunos:
        nome_limpo = aluno.nome.lower().replace(' ', '.').replace('ã', 'a').replace('õ', 'o').replace('é', 'e').replace('í', 'i').replace('ú', 'u').replace('ç', 'c')
        aluno.email = f"{nome_limpo}@escolaexemplo.com.br"
        aluno.telefone = "(85) 9" + "".join([str(i) for i in sample(range(10), 8)])
        if not aluno.matricula:
            aluno.matricula = f"MAT{aluno.id:06d}"
        aluno.save()
    
    print("✅ Todos os alunos com email, telefone e matrícula definidos!")
    
    # Seleciona 20 alunos para SEM EMAIL
    alunos_sem_email = sample(alunos, 20)
    for aluno in alunos_sem_email:
        aluno.email = ""
        aluno.save()
    
    print(f"✅ {len(alunos_sem_email)} alunos SEM EMAIL definidos!")
    
    # Seleciona 20 alunos para SEM TELEFONE
    alunos_sem_telefone = sample([a for a in alunos if a not in alunos_sem_email], 20)
    for aluno in alunos_sem_telefone:
        aluno.telefone = ""
        aluno.save()
    
    print(f"✅ {len(alunos_sem_telefone)} alunos SEM TELEFONE definidos!")
    
    # Seleciona 20 alunos para SEM MATRÍCULA
    alunos_sem_matricula = sample([a for a in alunos if a not in alunos_sem_email and a not in alunos_sem_telefone], 20)
    for aluno in alunos_sem_matricula:
        aluno.matricula = ""
        aluno.save()
    
    print(f"✅ {len(alunos_sem_matricula)} alunos SEM MATRÍCULA definidos!")
    
    print("\n📊 Resumo final:")
    print(f"  Total de alunos: {Aluno.objects.count()}")
    print(f"  Sem email: {Aluno.objects.filter(email='').count()}")
    print(f"  Sem telefone: {Aluno.objects.filter(telefone='').count()}")
    print(f"  Sem matrícula: {Aluno.objects.filter(matricula='').count()}")


if __name__ == "__main__":
    main()
