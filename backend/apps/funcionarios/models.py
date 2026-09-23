from django.db import models
from apps.usuarios.models import TimeStampedModel


class Funcionario(TimeStampedModel):
    """Modelo de funcionários da escola"""
    
    CARGO_CHOICES = [
        ('professor', 'Professor'),
        ('coordenador', 'Coordenador'),
        ('diretor', 'Diretor'),
        ('administrativo', 'Administrativo'),
        ('outro', 'Outro'),
    ]
    
    DEPARTAMENTO_CHOICES = [
        ('exatas', 'Exatas'),
        ('humanas', 'Humanas'),
        ('artes', 'Artes'),
        ('pedagogico', 'Pedagógico'),
        ('administrativo', 'Administrativo'),
    ]
    
    CARGA_CHOICES = [(40, '40h'), (44, '44h')]
    
    id_func = models.CharField(max_length=20, unique=True, verbose_name='ID Funcional')
    nome = models.CharField(max_length=150, verbose_name='Nome Completo')
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, verbose_name='Cargo')
    departamento = models.CharField(max_length=20, choices=DEPARTAMENTO_CHOICES, blank=True, verbose_name='Departamento')
    carga_horaria = models.IntegerField(choices=CARGA_CHOICES, default=40, verbose_name='Carga Horária')
    salario_base = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='Salário Base')
    salario_obs = models.CharField(max_length=100, blank=True, verbose_name='Observações do Salário')
    data_admissao = models.DateField(null=True, blank=True, verbose_name='Data de Admissão')
    data_admissao_obs = models.CharField(max_length=100, blank=True, verbose_name='Observações da Admissão')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ('nome',)
        indexes = [
            models.Index(fields=['id_func']),
            models.Index(fields=['nome']),
        ]
    
    def __str__(self):
        return f"{self.id_func} - {self.nome}"
    
    @property
    def salario_display(self):
        if self.salario_base:
            return f"R$ {self.salario_base:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return self.salario_obs or "Não informado"
