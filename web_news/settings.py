import os
from dotenv import load_dotenv
from pathlib import Path

# Carregar variáveis do arquivo .env
load_dotenv()

# Caminho do diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-8-5bmwyb4h8^j&f5^^t_@!^31lp58z9$6mzc8b+po$7ha)%)&x'
DEBUG = True
ALLOWED_HOSTS = []

# Banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
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
    'trendfeeds',
]

# User model
AUTH_USER_MODEL = 'trendfeeds.Usuarios'

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
        'DIRS': [os.path.join(BASE_DIR, 'trendfeeds', 'templates')],  # Ajuste para a pasta de templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  

            ],
        },
    },
]

# Timezone e Internacionalização
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos
# Configuração do caminho para arquivos estáticos
STATIC_URL = '/static/'

# Diretórios adicionais onde o Django vai procurar arquivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Diretório global de arquivos estáticos
    
    # Se os arquivos estáticos estão dentro de um app (exemplo: trendfeeds/static)
    BASE_DIR / "trendfeeds/static",  
]
# Arquivos estáticos coletados para produção
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Pasta onde os arquivos estáticos serão coletados para produção

# Arquivos de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Definição de chave primária
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROOT_URLCONF = 'web_news.urls'
