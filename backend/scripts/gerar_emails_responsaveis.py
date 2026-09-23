
import os
import django
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.alunos.models import Aluno


def main():
    # Pega todos os alunos
    alunos = list(Aluno.objects.all())
    
    total_atualizados = 0
    
    for aluno in alunos:
        # Se não tem email do responsável, cria um
        if not aluno.responsavel_email and aluno.responsavel_nome:
            # Cria email baseado no nome do responsável
            nome_limpo = aluno.responsavel_nome.lower().replace(' ', '.').replace('ã', 'a').replace('õ', 'o').replace('é', 'e').replace('í', 'i').replace('ú', 'u').replace('ç', 'c')
            aluno.responsavel_email = f"{nome_limpo}@escolaexemplo.com.br"
            aluno.save()
            total_atualizados += 1
    
    print(f"{total_atualizados} emails de responsaveis criados!")
    print(f"Total de alunos: {len(alunos)}")
    print(f"Alunos sem email de responsavel: {Aluno.objects.filter(responsavel_email='').count()}")


if __name__ == "__main__":
    main()
