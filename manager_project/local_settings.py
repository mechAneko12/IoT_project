import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'manager_project',
        'USER': 'mechAneko',
        'PASSWORD': 'Naoki0827',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DEBUG = True