from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index, name='index'),
    path('relatorio-inconsistencias/', views.relatorio_inconsistencias, name='relatorio_inconsistencias'),
]
