from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.alunos.models import Aluno
from apps.professores.models import Professor
from apps.turmas.models import Turma
from apps.notas.models import Nota
from apps.funcionarios.models import Funcionario


@login_required
def dashboard_index(request):
    """Dashboard principal do sistema com estatísticas"""
    # Contar dados
    total_alunos = Aluno.objects.filter(ativo=True).count()
    total_professores = Professor.objects.filter(ativo=True).count()
    total_funcionarios = Funcionario.objects.filter(ativo=True).count()
    total_turmas = Turma.objects.filter(ativa=True).count()
    
    context = {
        'total_alunos': total_alunos,
        'total_professores': total_professores,
        'total_funcionarios': total_funcionarios,
        'total_turmas': total_turmas,
    }
    
    return render(request, 'dashboard/index.html', context)


@login_required
def relatorio_inconsistencias(request):
    """Relatório de inconsistências nos dados"""
    # Alunos com inconsistências
    alunos_inconsistentes = []
    for aluno in Aluno.objects.all().order_by('matricula'):
        problemas = []
        if not aluno.email:
            problemas.append("Email não informado")
        if not aluno.telefone:
            problemas.append("Telefone não informado")
        if not aluno.responsavel_nome:
            problemas.append("Responsável não informado")
        if not aluno.responsavel_email:
            problemas.append("Email do responsável não informado")
        if not aluno.cpf:
            problemas.append("CPF não informado")
        if not aluno.matricula:
            problemas.append("Matrícula não informada")
        if not aluno.data_nascimento:
            problemas.append("Data de nascimento não informada")
        if not aluno.responsavel_telefone:
            problemas.append("Telefone do responsável não informado")
        if not aluno.endereco or aluno.endereco.lower() in ["fortaleza", "não consta", ""]:
            problemas.append("Endereço incompleto ou genérico")
        if len(aluno.nome.split()) < 2 or "." in aluno.nome:
            problemas.append("Nome abreviado ou incompleto")
        
        if problemas:
            alunos_inconsistentes.append({
                'matricula': aluno.matricula or "N/A",
                'nome': aluno.nome,
                'problemas': problemas,
                'aluno_obj': aluno
            })
    
    # Professores com inconsistências
    professores_inconsistentes = []
    for prof in Professor.objects.select_related('usuario').all():
        problemas = []
        if not prof.turmas.exists():
            problemas.append("Sem turmas atribuídas")
        if not prof.carga_horaria or prof.carga_horaria <= 0:
            problemas.append("Carga horária não informada")
        if not prof.disciplina or prof.disciplina.strip() == "":
            problemas.append("Disciplina não informada")
        
        if problemas:
            professores_inconsistentes.append({
                'nome': prof.usuario.get_full_name(),
                'disciplina': prof.disciplina or "N/A",
                'problemas': problemas,
                'prof_obj': prof
            })
    
    # Funcionários com inconsistências
    funcionarios_inconsistentes = []
    for func in Funcionario.objects.filter(ativo=True):
        problemas = []
        if not func.salario_base:
            problemas.append(f"Salário: {func.salario_obs or 'Não informado'}")
        if not func.data_admissao:
            problemas.append(f"Data de admissão: {func.data_admissao_obs or 'Não informado'}")
        
        if problemas:
            funcionarios_inconsistentes.append({
                'id_func': func.id_func,
                'nome': func.nome,
                'cargo': func.get_cargo_display(),
                'problemas': problemas,
                'func_obj': func
            })
    
    # Notas com inconsistências
    notas_inconsistentes = []
    from apps.notas.models import Nota
    for nota in Nota.objects.select_related('aluno', 'turma', 'professor').all():
        problemas = []
        # Verificar notas fora do intervalo 0-10
        for i, nota_valor in enumerate([nota.nota_1, nota.nota_2, nota.nota_3, nota.nota_4], 1):
            if nota_valor is not None:
                if nota_valor > 10 or nota_valor < 0:
                    problemas.append(f"{i}º Bimestre: {nota_valor} (fora de 0-10)")
        # Verificar disciplinas com nomes inconsistentes
        if nota.disciplina.lower() in ["port", "portugues", "fisica", "matemática (rec)"]:
            problemas.append(f"Disciplina '{nota.disciplina}' — padronizar")
        
        if problemas:
            notas_inconsistentes.append({
                'aluno_nome': nota.aluno.nome,
                'turma': nota.turma.__str__(),
                'disciplina': nota.disciplina,
                'problemas': problemas,
                'nota_obj': nota
            })
    
    # Verificar alunos em múltiplas turmas (mesmo nome em turmas diferentes)
    alunos_multiturmas = {}
    
    # Tarefas pendentes
    tarefas = []
    for a in alunos_inconsistentes:
        if "Nome abreviado" in str(a['problemas']):
            tarefas.append({
                'descricao': f"Confirmar nome completo de {a['nome']}",
                'tipo': 'aluno',
                'objeto': a['aluno_obj']
            })
        if "Email não informado" in str(a['problemas']):
            tarefas.append({
                'descricao': f"Informar email de {a['nome']}",
                'tipo': 'aluno',
                'objeto': a['aluno_obj']
            })
        if "Telefone não informado" in str(a['problemas']):
            tarefas.append({
                'descricao': f"Informar telefone de {a['nome']}",
                'tipo': 'aluno',
                'objeto': a['aluno_obj']
            })
        if "Responsável não informado" in str(a['problemas']):
            tarefas.append({
                'descricao': f"Informar responsável de {a['nome']}",
                'tipo': 'aluno',
                'objeto': a['aluno_obj']
            })
        if "Email do responsável não informado" in str(a['problemas']):
            tarefas.append({
                'descricao': f"Informar email do responsável de {a['nome']}",
                'tipo': 'aluno',
                'objeto': a['aluno_obj']
            })
        if "CPF não informado" in str(a['problemas']):
            tarefas.append({
                'descricao': f"Informar CPF de {a['nome']}",
                'tipo': 'aluno',
                'objeto': a['aluno_obj']
            })
        if "Matrícula não informada" in str(a['problemas']):
            tarefas.append({
                'descricao': f"Informar matrícula de {a['nome']}",
                'tipo': 'aluno',
                'objeto': a['aluno_obj']
            })
        if "Data de nascimento não informada" in str(a['problemas']):
            tarefas.append({
                'descricao': f"Informar data de nascimento de {a['nome']}",
                'tipo': 'aluno',
                'objeto': a['aluno_obj']
            })
        if "Endereço" in str(a['problemas']):
            tarefas.append({
                'descricao': f"Atualizar endereço de {a['nome']}",
                'tipo': 'aluno',
                'objeto': a['aluno_obj']
            })
        if "Telefone do responsável" in str(a['problemas']):
            tarefas.append({
                'descricao': f"Informar telefone do responsável de {a['nome']}",
                'tipo': 'aluno',
                'objeto': a['aluno_obj']
            })
    
    for p in professores_inconsistentes:
        for problema in p['problemas']:
            tarefas.append({
                'descricao': f"{problema} ({p['nome']})",
                'tipo': 'professor',
                'objeto': p['prof_obj']
            })
    
    for f in funcionarios_inconsistentes:
        for problema in f['problemas']:
            tarefas.append({
                'descricao': f"{problema} ({f['nome']} - {f['id_func']})",
                'tipo': 'funcionario',
                'objeto': f['func_obj']
            })
    
    for n in notas_inconsistentes:
        tarefas.append({
            'descricao': f"Corrigir notas de {n['aluno_nome']} ({n['disciplina']})",
            'tipo': 'nota',
            'objeto': n['nota_obj']
        })
    
    context = {
        'alunos_inconsistentes': alunos_inconsistentes,
        'professores_inconsistentes': professores_inconsistentes,
        'funcionarios_inconsistentes': funcionarios_inconsistentes,
        'notas_inconsistentes': notas_inconsistentes,
        'alunos_multiturmas': alunos_multiturmas,
        'tarefas': tarefas,
        'total_inconsistencias': (len(alunos_inconsistentes) + 
                                  len(professores_inconsistentes) + 
                                  len(funcionarios_inconsistentes) + 
                                  len(notas_inconsistentes)),
    }
    
    return render(request, 'dashboard/relatorio_inconsistencias.html', context)
