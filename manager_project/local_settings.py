import os

#settings.pyからそのままコピー
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '5d!x&vs&yo717sno(w%*ckie5$8wwb*k(+loe7n2sa%f)lw$i+'

#settings.pyからそのままコピー
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True #ローカルでDebugできるようになります
