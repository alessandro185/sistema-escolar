from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    path('', views.lista_notas, name='lista'),
    path('lancar/', views.lancar_nota, name='lancar'),
    path('lancar/<int:aluno_id>/', views.lancar_nota, name='lancar_aluno'),
    path('aluno/<int:aluno_id>/', views.notas_aluno, name='aluno'),
]
