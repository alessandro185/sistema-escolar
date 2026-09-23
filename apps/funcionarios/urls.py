from django.urls import path
from . import views

app_name = 'funcionarios'

urlpatterns = [
    path('', views.lista_funcionarios, name='lista'),
    path('<int:pk>/', views.detalhe_funcionario, name='detalhe'),
]
