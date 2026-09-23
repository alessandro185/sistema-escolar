from django import forms
from .models import Turma


class TurmaForm(forms.ModelForm):
    """Formulário para criação e edição de turmas"""
    
    class Meta:
        model = Turma
        fields = ['ano', 'letra', 'ano_letivo', 'ativa']
        widgets = {
            'ano': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'letra': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'ano_letivo': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'ativa': forms.CheckboxInput(attrs={'class': 'h-4 w-4'}),
        }
