# blog/blog/configurations/local.py
from .base import *
DEBUG = True # Modo de depuración activado, mostrará detalles de errores en la página
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# Configuraciones de base de datos de desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Puerto para entorno local
os.environ['DJANGO_PORT'] = '8000'
