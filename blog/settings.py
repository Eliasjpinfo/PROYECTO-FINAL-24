import os
from dotenv import load_dotenv

load_dotenv()

DJANGO_ENV = os.getenv('DJANGO_ENV', 'development')

if DJANGO_ENV == 'production':
    from.configuraciones.production import *
else:
    from.configuraciones.local import *


CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Link', 'Unlink', 'Image'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'Undo', 'Redo'],
        ],
        'height': 300,
        'width': '100%',
    },
}
