from .base import *

#デバッグモードを有効化。エラー発生時にブラウザ上にエラーの詳細情報を表示する。
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}