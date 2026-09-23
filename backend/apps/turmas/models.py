from django.db import models
from apps.usuarios.models import TimeStampedModel


class Turma(TimeStampedModel):
    """Modelo de turmas (1A, 1B, 2A, etc)"""
    ANO_CHOICES = [
        (1, '1º Ano'),
        (2, '2º Ano'),
        (3, '3º Ano'),
    ]
    
    LETRA_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
    
    ano = models.IntegerField(choices=ANO_CHOICES, verbose_name='Ano')
    letra = models.CharField(max_length=1, choices=LETRA_CHOICES, verbose_name='Letra')
    ano_letivo = models.IntegerField(default=2024, verbose_name='Ano Letivo')
    ativa = models.BooleanField(default=True, verbose_name='Ativa')
    
    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        unique_together = ('ano', 'letra', 'ano_letivo')
        ordering = ('ano', 'letra')
    
    def __str__(self):
        return f"{self.ano}º Ano - Turma {self.letra} ({self.ano_letivo})"
    
    def contar_alunos(self):
        """Retorna a quantidade de alunos na turma"""
        from apps.alunos.models import Aluno
        return Aluno.objects.filter(turma=self, ativo=True).count()
    
    def get_professores(self):
        """Retorna todos os professores da turma"""
        return self.professores.filter(ativo=True).all()
