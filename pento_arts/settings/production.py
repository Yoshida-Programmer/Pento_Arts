from .base import *

#デバッグモードを有効化。エラー発生時にブラウザ上にエラーの詳細情報を表示する。
DEBUG = False

# heroku側のDBはPostgreqlが推奨されているので、heroku側に合わせて設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': '',
        'HOST': 'host',
        'PORT': '',
    }
}

import dj_database_url

# DATABASESの欄で空欄のところは、おそらくこの2行で上書き
db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
DATABASES['default'].update(db_from_env)

django_heroku.settings(locals())