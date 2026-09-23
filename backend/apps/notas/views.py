from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Nota
from apps.alunos.models import Aluno
from apps.turmas.models import Turma
from .forms import NotaForm


@login_required
def lista_notas(request):
    """Listagem de notas com filtros"""
    notas = Nota.objects.all()
    
    # Filtrar por turma
    if request.GET.get('turma'):
        turma_id = request.GET.get('turma')
        notas = notas.filter(turma_id=turma_id)
    
    # Filtrar por aluno
    if request.GET.get('aluno'):
        aluno_id = request.GET.get('aluno')
        notas = notas.filter(aluno_id=aluno_id)
    
    # Filtrar por situação
    if request.GET.get('situacao'):
        situacao = request.GET.get('situacao')
        notas = notas.filter(situacao=situacao)
    
    turmas = Turma.objects.filter(ativa=True)
    
    context = {
        'notas': notas.order_by('-criado_em'),
        'turmas': turmas,
    }
    return render(request, 'notas/lista.html', context)


@login_required
def notas_aluno(request, aluno_id):
    """Notas de um aluno específico"""
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    notas = aluno.notas.all().order_by('-criado_em')
    
    # Calcular média geral
    media_geral = 0
    if notas.exists():
        media_geral = sum(nota.media for nota in notas) / notas.count()
    
    context = {
        'aluno': aluno,
        'notas': notas,
        'media_geral': round(media_geral, 2),
    }
    return render(request, 'notas/aluno.html', context)


@login_required
def lancar_nota(request, aluno_id=None):
    """Lançar/editar nota"""
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save()
            messages.success(request, 'Nota lançada/atualizada com sucesso!')
            return redirect('notas:aluno', aluno_id=nota.aluno.id)
    else:
        initial = {}
        if aluno_id:
            initial['aluno'] = Aluno.objects.get(pk=aluno_id)
        form = NotaForm(initial=initial)
    
    context = {'form': form}
    return render(request, 'notas/form.html', context)
