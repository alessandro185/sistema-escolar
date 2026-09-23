from django.urls import path
from . import views

app_name = 'professores'

urlpatterns = [
    path('', views.lista_professores, name='lista'),
    path('criar/', views.criar_professor, name='criar'),
    path('<int:pk>/', views.detalhes_professor, name='detalhes'),
    path('<int:pk>/editar/', views.editar_professor, name='editar'),
]
