from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Professor
from .forms import ProfessorForm


@login_required
def lista_professores(request):
    """Listagem de professores"""
    busca = request.GET.get('busca', '')
    professores = Professor.objects.all()
    
    if busca:
        professores = professores.filter(
            Q(usuario__first_name__icontains=busca) |
            Q(usuario__last_name__icontains=busca) |
            Q(disciplina__icontains=busca)
        )
    
    paginator = Paginator(professores.order_by('usuario__first_name'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'professores': page_obj.object_list,
        'busca': busca,
    }
    return render(request, 'professores/lista.html', context)


@login_required
def detalhes_professor(request, pk):
    """Detalhes de um professor"""
    professor = get_object_or_404(Professor, pk=pk)
    turmas = professor.turmas.all()
    notas = professor.notas.all()
    
    context = {
        'professor': professor,
        'turmas': turmas,
        'notas': notas,
    }
    return render(request, 'professores/detalhes.html', context)


@login_required
def criar_professor(request):
    """Criar novo professor"""
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professor criado com sucesso!')
            return redirect('professores:lista')
    else:
        form = ProfessorForm()
    
    context = {'form': form}
    return render(request, 'professores/form.html', context)


@login_required
def editar_professor(request, pk):
    """Editar professor"""
    professor = get_object_or_404(Professor, pk=pk)
    
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professor atualizado com sucesso!')
            return redirect('professores:detalhes', pk=professor.pk)
    else:
        form = ProfessorForm(instance=professor)
    
    context = {'form': form, 'professor': professor}
    return render(request, 'professores/form.html', context)
