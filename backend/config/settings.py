"""
Django settings for escola_sistema project.
"""

import os
import sys
from pathlib import Path
from decouple import config, Csv
from django.core.management.utils import get_random_secret_key
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
# Localmente, crie um arquivo .env com DEBUG=True. Em produção (Vercel) não defina.
DEBUG = config('DEBUG', default=False, cast=bool)

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-only-key')
else:
    SECRET_KEY = config('SECRET_KEY', default='')
    if not SECRET_KEY:
        # Não derruba o build/deploy: gera chave temporária e avisa.
        # Defina SECRET_KEY nas variáveis de ambiente da Vercel.
        print('AVISO: SECRET_KEY nao definida; usando chave temporaria.', file=sys.stderr)
        SECRET_KEY = get_random_secret_key()

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1,.vercel.app',
    cast=Csv(),
)

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://*.vercel.app',
    cast=Csv(),
)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'crispy_forms',
    'crispy_tailwind',
    'django_filters',
    
    # Local apps
    'apps.usuarios.apps.UsuariosConfig',
    'apps.alunos.apps.AlunosConfig',
    'apps.professores.apps.ProfessoresConfig',
    'apps.turmas.apps.TurmasConfig',
    'apps.notas.apps.NotasConfig',
    'apps.dashboard.apps.DashboardConfig',
    'apps.funcionarios.apps.FuncionariosConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.parent / 'frontend' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.usuarios.context_processors.cargo_usuario',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# Em produção defina DATABASE_URL (ex.: postgresql://user:senha@host/db?sslmode=require).
# Sem DATABASE_URL, usa SQLite local na raiz do repositório.


def _limpar_database_url(valor):
    """Remove erros comuns de copia: espacos, aspas e o prefixo 'psql'."""
    if not valor:
        return None
    valor = valor.strip()
    if valor.lower().startswith('psql'):
        valor = valor[4:].strip()
    return valor.strip('\'"').strip() or None


DATABASE_URL = _limpar_database_url(config('DATABASE_URL', default=None))
if not DATABASE_URL:
    if DEBUG:
        DATABASE_URL = f"sqlite:///{BASE_DIR.parent / 'db.sqlite3'}"
    else:
        # Não derruba o build/deploy; o site sobe, mas sem banco persistente.
        print('AVISO: DATABASE_URL nao definida; defina um PostgreSQL na Vercel.', file=sys.stderr)
        DATABASE_URL = 'sqlite:////tmp/db.sqlite3'

DATABASES = {
    'default': dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=0,  # serverless: não reaproveitar conexões entre invocações
    )
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
FRONTEND_STATIC_DIR = BASE_DIR.parent / 'frontend' / 'static'
STATICFILES_DIRS = [FRONTEND_STATIC_DIR] if FRONTEND_STATIC_DIR.exists() else []

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
}

# Media files (User uploads - Fotos dos alunos)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Login URL
LOGIN_URL = 'usuarios:login'
LOGIN_REDIRECT_URL = 'dashboard:index'

# Session
SESSION_COOKIE_AGE = 86400  # 24 horas
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Segurança em produção
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
        'SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool
    )

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
