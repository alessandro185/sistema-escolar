from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.usuarios.models import TimeStampedModel


class Nota(TimeStampedModel):
    """Modelo de notas dos alunos"""
    from apps.alunos.models import Aluno
    from apps.professores.models import Professor
    
    aluno = models.ForeignKey(
        'alunos.Aluno',
        on_delete=models.CASCADE,
        related_name='notas',
        verbose_name='Aluno'
    )
    professor = models.ForeignKey(
        'professores.Professor',
        on_delete=models.SET_NULL,
        null=True,
        related_name='notas',
        verbose_name='Professor'
    )
    turma = models.ForeignKey(
        'turmas.Turma',
        on_delete=models.CASCADE,
        related_name='notas',
        verbose_name='Turma'
    )
    disciplina = models.CharField(max_length=100, verbose_name='Disciplina')
    
    # Notas (4 bimestres)
    nota_1 = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='1º Bimestre'
    )
    nota_2 = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='2º Bimestre'
    )
    nota_3 = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='3º Bimestre'
    )
    nota_4 = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='4º Bimestre'
    )
    
    media = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name='Média Anual')
    
    # Situação
    SITUACAO_CHOICES = [
        ('ativo', 'Ativo'),
        ('aprovado', 'Aprovado'),
        ('reprovado', 'Reprovado'),
        ('transferido', 'Transferido'),
    ]
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES, default='ativo', verbose_name='Situação')
    
    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        unique_together = ('aluno', 'professor', 'turma')
        ordering = ('aluno__nome',)
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.disciplina} - Média: {self.media}"
    
    def calcular_media(self):
        """Calcula a média automática do aluno"""
        notas = [n for n in [self.nota_1, self.nota_2, self.nota_3, self.nota_4] if n is not None]
        
        if notas:
            self.media = sum(notas) / len(notas)
            return self.media
        return 0
    
    def save(self, *args, **kwargs):
        """Calcula a média ao salvar"""
        self.calcular_media()
        super().save(*args, **kwargs)
