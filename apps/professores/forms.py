from django import forms
from .models import Professor


class ProfessorForm(forms.ModelForm):
    """Formulário para cadastro e edição de professores"""
    
    class Meta:
        model = Professor
        fields = ['usuario', 'disciplina', 'carga_horaria', 'turmas', 'ativo']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'disciplina': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Ex: Matemática'}),
            'carga_horaria': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Horas por semana'}),
            'turmas': forms.CheckboxSelectMultiple(attrs={'class': 'space-y-2'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'h-4 w-4'}),
        }
