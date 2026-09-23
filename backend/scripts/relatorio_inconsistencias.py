
import os
import django
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.alunos.models import Aluno
from apps.professores.models import Professor

print("=" * 80)
print("[CONTROLE DE ALUNOS] RELATORIO DE INCONSISTENCIAS - PLANILHAS DA ESCOLA")
print("=" * 80)

print("\n[ALUNOS]")
print("-" * 80)
alunos_inconsistentes = []
for aluno in Aluno.objects.all().order_by('matricula'):
    problemas = []
    if not aluno.responsavel_telefone:
        problemas.append("Telefone do responsavel nao informado")
    if not aluno.endereco or aluno.endereco.lower() in ["fortaleza", "nao consta", ""]:
        problemas.append("Endereco incompleto ou generico")
    if len(aluno.nome.split()) < 2 or "." in aluno.nome:
        problemas.append("Nome abreviado ou incompleto")
    
    if problemas:
        alunos_inconsistentes.append({
            'matricula': aluno.matricula,
            'nome': aluno.nome,
            'problemas': problemas
        })

if alunos_inconsistentes:
    print(f"{'Matricula':<12} {'Nome':<30} {'Problemas'}")
    print("-" * 80)
    for a in alunos_inconsistentes:
        print(f"{a['matricula']:<12} {a['nome']:<30} {', '.join(a['problemas'])}")
else:
    print("[OK] Nenhum aluno com inconsistencias encontrado!")

print("\n[PROFESSORES]")
print("-" * 80)
professores_inconsistentes = []
for prof in Professor.objects.select_related('usuario').all():
    problemas = []
    if not prof.carga_horaria or prof.carga_horaria <= 0:
        problemas.append("Carga horaria nao informada")
    
    if problemas:
        professores_inconsistentes.append({
            'nome': prof.usuario.get_full_name(),
            'disciplina': prof.disciplina,
            'problemas': problemas
        })

if professores_inconsistentes:
    print(f"{'Nome':<30} {'Disciplina':<20} {'Problemas'}")
    print("-" * 80)
    for p in professores_inconsistentes:
        print(f"{p['nome']:<30} {p['disciplina']:<20} {', '.join(p['problemas'])}")
else:
    print("[OK] Nenhum professor com inconsistencias encontrado!")

print("\n[PENDENCIAS PARA A DIRETORA]")
print("-" * 80)
tarefas = []

for a in alunos_inconsistentes:
    if "Nome abreviado" in str(a['problemas']):
        tarefas.append(f"[ ] Confirmar nome completo de {a['nome']} (matricula {a['matricula']})")
    if "Endereco" in str(a['problemas']):
        tarefas.append(f"[ ] Atualizar endereco de {a['nome']}")
    if "Telefone" in str(a['problemas']):
        tarefas.append(f"[ ] Informar telefone de {a['nome']}")

if tarefas:
    for tarefa in tarefas:
        print(tarefa)
else:
    print("[OK] Nenhuma pendencia no momento!")

print("\n" + "=" * 80)
print("FIM DO RELATORIO")
print("=" * 80)
