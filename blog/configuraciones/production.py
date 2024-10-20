# blog/blog/configurations/production.py
from .base import *
DEBUG = False # Modo de depuración desactivado, no mostrará detalles de errores en la página
# TODO: Dejar solo el dominio de producción
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'production-domain.com']
# TODO: Cambiar la configuración de la base de datos para producción
# Configuraciones de base de datos de producción
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # En caso de usar postgresql
        # 'ENGINE': 'django.db.backends.postgresql',
        # En caso de usar mysql
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': os.getenv('DB_NAME'), # valor de la variable de entorno DB_NAME en el .env
        # 'USER': os.getenv('DB_USER'), # valor de la variable de entorno DB_USER en el .env
        # 'PASSWORD': os.getenv('DB_PASSWORD'), # valor de la variable de entorno DB_PASSWORD en el .env
        # 'HOST': os.getenv('DB_HOST'), # valor de la variable de entorno DB_HOST en el .env
        # 'PORT': os.getenv('DB_PORT'), # valor de la variable de entorno DB_PORT en el .env
    }
}
# Puerto para entorno de producción
os.environ['DJANGO_PORT'] = '8080'
