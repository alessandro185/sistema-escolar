from django.contrib import admin
from .models import Professor


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'disciplina', 'carga_horaria', 'ativo')
    list_filter = ('disciplina', 'ativo', 'criado_em')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'disciplina')
    readonly_fields = ('criado_em', 'atualizado_em')
    filter_horizontal = ('turmas',)
    
    fieldsets = (
        ('Usuário', {
            'fields': ('usuario',)
        }),
        ('Informações Profissionais', {
            'fields': ('disciplina', 'carga_horaria', 'turmas')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Auditoria', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
