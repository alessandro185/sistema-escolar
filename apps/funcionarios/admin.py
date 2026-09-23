from django.contrib import admin
from .models import Funcionario


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id_func', 'nome', 'cargo', 'departamento', 'ativo', 'salario_display', 'data_admissao')
    list_filter = ('cargo', 'departamento', 'ativo', 'carga_horaria')
    search_fields = ('id_func', 'nome')
    list_editable = ('ativo',)
    
    fieldsets = (
        ('Dados Básicos', {
            'fields': ('id_func', 'nome', 'ativo')
        }),
        ('Cargo e Departamento', {
            'fields': ('cargo', 'departamento', 'carga_horaria')
        }),
        ('Salário', {
            'fields': ('salario_base', 'salario_obs')
        }),
        ('Admissão', {
            'fields': ('data_admissao', 'data_admissao_obs')
        }),
        ('Datas de Sistema', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('criado_em', 'atualizado_em')
    
    def salario_display(self, obj):
        return obj.salario_display
    salario_display.short_description = 'Salário'
