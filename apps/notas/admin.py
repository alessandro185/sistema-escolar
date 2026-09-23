from django.contrib import admin
from .models import Nota


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'turma', 'disciplina', 'media', 'situacao')
    list_filter = ('situacao', 'criado_em', 'turma', 'disciplina')
    search_fields = ('aluno__nome', 'professor__usuario__first_name', 'disciplina')
    readonly_fields = ('media', 'criado_em', 'atualizado_em')
    
    fieldsets = (
        ('Aluno', {
            'fields': ('aluno', 'turma')
        }),
        ('Professor e Disciplina', {
            'fields': ('professor', 'disciplina')
        }),
        ('Notas', {
            'fields': ('nota_1', 'nota_2', 'nota_3', 'nota_4', 'media')
        }),
        ('Situação', {
            'fields': ('situacao',)
        }),
        ('Auditoria', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        obj.calcular_media()
        super().save_model(request, obj, form, change)
