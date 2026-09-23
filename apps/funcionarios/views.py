from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Funcionario


@login_required
def lista_funcionarios(request):
    """Listagem de funcionários com filtros"""
    funcionarios = Funcionario.objects.filter(ativo=True)
    
    # Filtros
    cargo = request.GET.get('cargo')
    departamento = request.GET.get('departamento')
    busca = request.GET.get('q')
    
    if cargo:
        funcionarios = funcionarios.filter(cargo=cargo)
    if departamento:
        funcionarios = funcionarios.filter(departamento=departamento)
    if busca:
        funcionarios = funcionarios.filter(
            Q(nome__icontains=busca) |
            Q(id_func__icontains=busca)
        )
    
    # Contagens
    total = funcionarios.count()
    contagem_por_cargo = Funcionario.objects.filter(ativo=True).values('cargo').annotate(total=Count('id'))
    
    # Verificar pendências
    tem_pendencias = Funcionario.objects.filter(
        Q(salario_base__isnull=True) |
        Q(data_admissao__isnull=True)
    ).exists()
    
    # Paginação
    paginator = Paginator(funcionarios.order_by('nome'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'funcionarios': page_obj.object_list,
        'total': total,
        'contagem_por_cargo': contagem_por_cargo,
        'tem_pendencias': tem_pendencias,
        'cargos': Funcionario.CARGO_CHOICES,
        'departamentos': Funcionario.DEPARTAMENTO_CHOICES,
        'cargo_selecionado': cargo,
        'departamento_selecionado': departamento,
        'busca': busca,
    }
    
    return render(request, 'funcionarios/lista.html', context)


@login_required
def detalhe_funcionario(request, pk):
    """Detalhes de um funcionário"""
    from datetime import date
    
    funcionario = get_object_or_404(Funcionario, pk=pk)
    
    # Verificar pendências
    pendencias = []
    if not funcionario.salario_base:
        pendencias.append(f"Salário: {funcionario.salario_obs or 'Não informado'}")
    if not funcionario.data_admissao:
        pendencias.append(f"Data de admissão: {funcionario.data_admissao_obs or 'Não informado'}")
    
    # Calcular anos de casa
    anos_casa = None
    if funcionario.data_admissao:
        hoje = date.today()
        anos_casa = hoje.year - funcionario.data_admissao.year - ((hoje.month, hoje.day) < (funcionario.data_admissao.month, funcionario.data_admissao.day))
    
    context = {
        'funcionario': funcionario,
        'pendencias': pendencias,
        'anos_casa': anos_casa,
    }
    
    return render(request, 'funcionarios/detalhe.html', context)
