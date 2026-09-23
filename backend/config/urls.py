"""
URL configuration for escola_sistema project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.dashboard.urls', namespace='dashboard')),
    path('usuarios/', include('apps.usuarios.urls', namespace='usuarios')),
    path('alunos/', include('apps.alunos.urls', namespace='alunos')),
    path('professores/', include('apps.professores.urls', namespace='professores')),
    path('funcionarios/', include('apps.funcionarios.urls', namespace='funcionarios')),
    path('turmas/', include('apps.turmas.urls', namespace='turmas')),
    path('notas/', include('apps.notas.urls', namespace='notas')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
