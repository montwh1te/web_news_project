import os
from dotenv import load_dotenv
from pathlib import Path

# Carregar variáveis do arquivo .env
load_dotenv()

# Caminho do diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'sua-chave-secreta-padrao')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}

# Aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'trendfeeds',
    'users',
    'api',
    'rest_framework',
]

# User model
AUTH_USER_MODEL = 'users.Usuarios'

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configurações de template
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates/html'),
            os.path.join(BASE_DIR, 'templates/html/noticias'),
            os.path.join(BASE_DIR, 'templates/users'),

            ],  # Diretório de templates
        'APP_DIRS': True,  # Isso permite que o Django procure também em pastas de templates dentro dos apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# Timezone e Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos
# Configuração do caminho para arquivos estáticos
STATIC_URL = '/static/'

# Diretórios adicionais onde o Django vai procurar arquivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / "trendfeeds/static",  # Diretório estático do app 'trendfeeds'
    BASE_DIR / "users/static",       # Diretório estático do app 'users'
]

# Arquivos estáticos coletados para produção
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Pasta onde os arquivos estáticos serão coletados para produção

# Arquivos de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'trendfeeds', 'media')

# Definição de chave primária
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROOT_URLCONF = 'web_news.urls'

API_FUTEBOL_KEY = 'live_ad0fd9ca24b96c2f806ad3cf2dd035'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Configuração máxima (2 GB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024 * 1024  # 100 GB
FILE_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024 * 1024  # 100 GB

