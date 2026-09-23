from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Turma
from apps.alunos.models import Aluno
from .forms import TurmaForm


@login_required
def lista_turmas(request):
    """Listagem de turmas"""
    turmas = Turma.objects.all().annotate(total_alunos=Count('alunos'))
    
    context = {
        'turmas': turmas.order_by('ano', 'letra'),
    }
    return render(request, 'turmas/lista.html', context)


@login_required
def detalhes_turma(request, pk):
    """Detalhes de uma turma com alunos"""
    turma = get_object_or_404(Turma, pk=pk)
    alunos = turma.alunos.filter(ativo=True).order_by('nome')
    professores = turma.professores.filter(ativo=True)
    
    context = {
        'turma': turma,
        'alunos': alunos,
        'professores': professores,
        'total_alunos': alunos.count(),
    }
    return render(request, 'turmas/detalhes.html', context)


@login_required
def criar_turma(request):
    """Criar nova turma"""
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save()
            messages.success(request, f'Turma {turma} criada com sucesso!')
            return redirect('turmas:detalhes', pk=turma.pk)
    else:
        form = TurmaForm()
    
    context = {'form': form}
    return render(request, 'turmas/form.html', context)


@login_required
def editar_turma(request, pk):
    """Editar turma"""
    turma = get_object_or_404(Turma, pk=pk)
    
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma atualizada com sucesso!')
            return redirect('turmas:detalhes', pk=turma.pk)
    else:
        form = TurmaForm(instance=turma)
    
    context = {'form': form, 'turma': turma}
    return render(request, 'turmas/form.html', context)
