from django.db import models
from django.contrib.auth.models import User
from apps.usuarios.models import TimeStampedModel


class Professor(TimeStampedModel):
    """Modelo de professores"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor')
    disciplina = models.CharField(max_length=100, verbose_name='Disciplina')
    carga_horaria = models.IntegerField(verbose_name='Carga Horária Semanal (horas)')
    turmas = models.ManyToManyField('turmas.Turma', related_name='professores', blank=True)
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'
        ordering = ('usuario__first_name',)
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.disciplina}"
    
    def get_turmas_display(self):
        """Retorna as turmas separadas por vírgula"""
        return ', '.join(str(turma) for turma in self.turmas.all())
