from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from .models import Aluno, Turma
from .forms import AlunoForm, AlunoSearchForm


@login_required
def lista_alunos(request):
    """Listagem de alunos com filtro por turma e status, ordenação e contagem por status"""
    form = AlunoSearchForm(request.GET)
    alunos = Aluno.objects.all()
    
    # Aplicar filtro de turma
    turma_id = request.GET.get('turma')
    if turma_id:
        alunos = alunos.filter(turma_id=turma_id)
    
    # Aplicar filtro de status (ativo/inativo)
    status = request.GET.get('status')
    if status == 'ativo':
        alunos = alunos.filter(ativo=True)
    elif status == 'inativo':
        alunos = alunos.filter(ativo=False)
    
    # Ordenar por turma e nome
    alunos = alunos.order_by('turma__ano', 'turma__letra', 'nome')
    
    # Contagem por status
    contagem_status = Aluno.objects.aggregate(
        total=Count('id'),
        ativos=Count('id', filter=Q(ativo=True)),
        inativos=Count('id', filter=Q(ativo=False))
    )
    
    # Paginar
    paginator = Paginator(alunos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'alunos': page_obj.object_list,
        'contagem_status': contagem_status,
        'turmas': Turma.objects.filter(ativa=True),
        'turma_selecionada': turma_id,
        'status_selecionado': status,
    }
    
    return render(request, 'alunos/lista.html', context)


@login_required
def detalhes_aluno(request, pk):
    """Detalhes de um aluno"""
    aluno = get_object_or_404(Aluno, pk=pk)
    notas = aluno.notas.all()
    
    context = {
        'aluno': aluno,
        'notas': notas,
    }
    
    return render(request, 'alunos/detalhes.html', context)


@login_required
def buscar_alunos(request):
    """Busca por nome ou matrícula - retorna JSON para AJAX"""
    busca = request.GET.get('q', '')
    if busca:
        alunos = Aluno.objects.filter(
            Q(nome__icontains=busca) |
            Q(matricula__icontains=busca)
        ).filter(ativo=True)[:10]
        
        resultados = []
        for aluno in alunos:
            resultados.append({
                'id': aluno.id,
                'nome': aluno.nome,
                'matricula': aluno.matricula,
                'turma': str(aluno.turma) if aluno.turma else '',
                'url': f'/alunos/{aluno.id}/'
            })
        
        return JsonResponse({'resultados': resultados})
    return JsonResponse({'resultados': []})


@login_required
def criar_aluno(request):
    """Criar novo aluno"""
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            aluno = form.save(commit=False)
            # Gerar matrícula automática
            if not aluno.matricula:
                ultimo = Aluno.objects.all().order_by('-id').first()
                aluno.matricula = f"MAT{ultimo.id + 1 if ultimo else 1:06d}"
            aluno.save()
            messages.success(request, f'Aluno {aluno.nome} criado com sucesso!')
            return redirect('alunos:detalhes', pk=aluno.pk)
    else:
        form = AlunoForm()
    
    context = {'form': form}
    return render(request, 'alunos/form.html', context)


@login_required
def editar_aluno(request, pk):
    """Editar aluno"""
    aluno = get_object_or_404(Aluno, pk=pk)
    
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno atualizado com sucesso!')
            return redirect('alunos:detalhes', pk=aluno.pk)
    else:
        form = AlunoForm(instance=aluno)
    
    context = {'form': form, 'aluno': aluno}
    return render(request, 'alunos/form.html', context)


@login_required
def deletar_aluno(request, pk):
    """Deletar aluno (soft delete - marcar como inativo)"""
    aluno = get_object_or_404(Aluno, pk=pk)
    
    if request.method == 'POST':
        aluno.ativo = False
        aluno.save()
        messages.success(request, f'Aluno {aluno.nome} removido com sucesso!')
        return redirect('alunos:lista')
    
    context = {'aluno': aluno}
    return render(request, 'alunos/confirmar_delecao.html', context)
