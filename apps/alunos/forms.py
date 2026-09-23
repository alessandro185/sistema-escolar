from django import forms
from .models import Aluno, Turma


class AlunoForm(forms.ModelForm):
    """Formulário para cadastro e edição de alunos"""
    
    class Meta:
        model = Aluno
        fields = [
            'nome', 'cpf', 'data_nascimento', 'genero', 'email', 'telefone',
            'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep',
            'responsavel_nome', 'responsavel_telefone', 'responsavel_email',
            'turma', 'matricula', 'foto', 'ativo'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'cpf': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg', 'placeholder': '000.000.000-00'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg', 'type': 'date'}),
            'genero': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'telefone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'endereco': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'numero': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'complemento': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'bairro': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'cidade': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'estado': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'cep': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'responsavel_nome': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'responsavel_telefone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'responsavel_email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'turma': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'matricula': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'foto': forms.FileInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg', 'accept': 'image/*'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'h-4 w-4'}),
        }


class AlunoSearchForm(forms.Form):
    """Formulário de busca de alunos"""
    busca = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
            'placeholder': 'Buscar por nome ou CPF...'
        })
    )
    turma = forms.ModelChoiceField(
        queryset=Turma.objects.none(),
        required=False,
        empty_label='Todas as turmas',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['turma'].queryset = Turma.objects.filter(ativa=True).order_by('ano', 'letra')
