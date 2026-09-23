from django.urls import path
from . import views

app_name = 'alunos'

urlpatterns = [
    path('', views.lista_alunos, name='lista'),
    path('criar/', views.criar_aluno, name='criar'),
    path('buscar/', views.buscar_alunos, name='buscar'),
    path('<int:pk>/', views.detalhes_aluno, name='detalhes'),
    path('<int:pk>/editar/', views.editar_aluno, name='editar'),
    path('<int:pk>/deletar/', views.deletar_aluno, name='deletar'),
]
