from django.urls import path
from . import views

app_name = 'turmas'

urlpatterns = [
    path('', views.lista_turmas, name='lista'),
    path('criar/', views.criar_turma, name='criar'),
    path('<int:pk>/', views.detalhes_turma, name='detalhes'),
    path('<int:pk>/editar/', views.editar_turma, name='editar'),
]
