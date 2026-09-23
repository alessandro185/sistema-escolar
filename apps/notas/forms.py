from django import forms
from .models import Nota


class NotaForm(forms.ModelForm):
    """Formulário para lançamento de notas"""
    
    class Meta:
        model = Nota
        fields = ['aluno', 'turma', 'professor', 'disciplina', 'nota_1', 'nota_2', 'nota_3', 'nota_4', 'situacao']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'turma': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'professor': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'disciplina': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Ex: Matemática'}),
            'nota_1': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg', 'min': 0, 'max': 10, 'step': 0.1}),
            'nota_2': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg', 'min': 0, 'max': 10, 'step': 0.1}),
            'nota_3': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg', 'min': 0, 'max': 10, 'step': 0.1}),
            'nota_4': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg', 'min': 0, 'max': 10, 'step': 0.1}),
            'situacao': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
        }
