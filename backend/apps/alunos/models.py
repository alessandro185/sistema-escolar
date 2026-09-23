from django.db import models
from apps.usuarios.models import TimeStampedModel
from apps.turmas.models import Turma


class Aluno(TimeStampedModel):
    """Modelo de alunos"""
    # Informações pessoais
    nome = models.CharField(max_length=150, verbose_name='Nome Completo')
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    genero = models.CharField(
        max_length=1,
        choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')],
        verbose_name='Gênero'
    )
    
    # Contato
    email = models.EmailField(blank=True, verbose_name='Email')
    telefone = models.CharField(max_length=15, blank=True, verbose_name='Telefone')
    
    # Endereço
    endereco = models.CharField(max_length=200, blank=True, verbose_name='Endereço')
    numero = models.CharField(max_length=10, blank=True, verbose_name='Número')
    complemento = models.CharField(max_length=100, blank=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=100, blank=True, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, blank=True, verbose_name='Cidade')
    estado = models.CharField(max_length=2, blank=True, verbose_name='Estado')
    cep = models.CharField(max_length=9, blank=True, verbose_name='CEP')
    
    # Responsáveis
    responsavel_nome = models.CharField(max_length=150, blank=True, verbose_name='Nome do Responsável')
    responsavel_telefone = models.CharField(max_length=15, blank=True, verbose_name='Telefone do Responsável')
    responsavel_email = models.EmailField(blank=True, verbose_name='Email do Responsável')
    
    # Escolar
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, related_name='alunos', verbose_name='Turma')
    matricula = models.CharField(max_length=20, unique=True, verbose_name='Matrícula')
    data_matricula = models.DateField(auto_now_add=True, verbose_name='Data de Matrícula')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    # Foto
    foto = models.ImageField(
        upload_to='alunos/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Foto'
    )
    
    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ('nome',)
        indexes = [
            models.Index(fields=['cpf']),
            models.Index(fields=['matricula']),
            models.Index(fields=['nome']),
        ]
    
    def __str__(self):
        return f"{self.nome} - {self.turma}"
