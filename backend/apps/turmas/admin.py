from django.contrib import admin
from .models import Turma


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'ano_letivo', 'ativa', 'contar_alunos')
    list_filter = ('ano', 'letra', 'ano_letivo', 'ativa')
    search_fields = ('ano', 'letra')
    readonly_fields = ('criado_em', 'atualizado_em')
    filter_horizontal = ('professores',)
    
    fieldsets = (
        ('Informações da Turma', {
            'fields': ('ano', 'letra', 'ano_letivo', 'ativa')
        }),
        ('Professores', {
            'fields': ('professores',)
        }),
        ('Auditoria', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )

