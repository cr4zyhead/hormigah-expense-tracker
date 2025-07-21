"""
Configuraciones de Django para el entorno de desarrollo local.
"""

import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', 'web']

# Base de datos para desarrollo local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'gastos_hormiga_dev'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Configuraciones de desarrollo
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configuración de logging para desarrollo
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
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Django Debug Toolbar (opcional para desarrollo)
if DEBUG:
    try:
        import debug_toolbar
        INSTALLED_APPS += ['debug_toolbar']
        MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
        
        # Configuración mejorada para Docker
        INTERNAL_IPS = [
            '127.0.0.1',
            'localhost',
        ]
        
        # Para Docker: detectar automáticamente la IP del gateway
        import socket
        hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
        INTERNAL_IPS += [ip[: ip.rfind(".")] + ".1" for ip in ips]
        
        # Rangos comunes de Docker
        INTERNAL_IPS += ['172.17.0.1', '172.18.0.1', '172.19.0.1', '172.20.0.1']
        
    except ImportError:
        pass

# Configuración de n8n para desarrollo
N8N_BASE_URL = os.getenv('N8N_BASE_URL', 'http://localhost:5678')

# Bearer Token para autenticación de webhooks con n8n
# En desarrollo puede ser un token simple
N8N_WEBHOOK_TOKEN = os.getenv('N8N_WEBHOOK_TOKEN', 'dev-token-123')

# Bearer Token para autenticación de API REST con n8n
# Token separado para mayor seguridad
N8N_API_TOKEN = os.getenv('N8N_API_TOKEN', 'dev-api-token-123') 