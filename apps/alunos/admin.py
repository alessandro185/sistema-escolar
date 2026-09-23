from django.contrib import admin
from django.utils.html import format_html
from .models import Aluno


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'turma', 'matricula', 'ativo', 'thumbnail_foto')
    list_filter = ('turma', 'ativo', 'genero', 'criado_em')
    search_fields = ('nome', 'cpf', 'matricula', 'email')
    readonly_fields = ('matricula', 'data_matricula', 'criado_em', 'atualizado_em', 'foto_preview')
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'cpf', 'data_nascimento', 'genero', 'foto', 'foto_preview')
        }),
        ('Contato', {
            'fields': ('email', 'telefone')
        }),
        ('Endereço', {
            'fields': ('endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep'),
            'classes': ('collapse',)
        }),
        ('Responsáveis', {
            'fields': ('responsavel_nome', 'responsavel_telefone', 'responsavel_email'),
            'classes': ('collapse',)
        }),
        ('Informações Escolares', {
            'fields': ('turma', 'matricula', 'data_matricula', 'ativo')
        }),
        ('Auditoria', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def thumbnail_foto(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.foto.url)
        return '-'
    thumbnail_foto.short_description = 'Foto'
    
    def foto_preview(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="200" />', obj.foto.url)
        return 'Nenhuma foto'
    foto_preview.short_description = 'Visualização da Foto'

