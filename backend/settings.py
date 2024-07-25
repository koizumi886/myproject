"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y+w8ki0tp25fd728f&k6mgoobb1i45890)y^l#)u7!4*idrf9c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # 追加
    'rest_framework.authtoken', #　認証トークン
    'app', # 追加
    'corsheaders', # 追加
    'accounts', # 追加
    'poem', # 追加
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # 追加
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"], # 追加
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'ATOMIC_REQUESTS': True,  # 追加
    },
    # 以下はデフォ
    # 'OPTIONS': {
    #     'isolation_level': 'READ COMMITTED',
    # },
}


# Password validation　パスワードのバリデーションルール
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'dist/static']  # 追加
MEDIA_URL = '/media/' # 画像ファイルを参照するためのURL
MEDIA_ROOT = BASE_DIR / 'media' # 画像保存先ディレクトリ

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# すべてのURLを許可する場合Trueを設定
# CORS_ALLOW_ALL_ORIGINS = True

# 信頼できる発信元リストに、Vueのオリジンを追加
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8080',
    'http://127.0.0.1:8000',
    'http://localhost:8080',
    'http://localhost:8000',
    ]

# 自身以外のオリジンのHTTPリクエスト内にクッキーを含めることを許可する
CORS_ALLOW_CREDENTIALS = True

# アクセスを許可したいURL（アクセス元）を追加
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8080',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://localhost:8080',
    # 'https://33f9-2001-268-c141-cacb-196d-d0be-567c-f2a4.ngrok-free.app',
    # 他の許可したいドメインを追加
]
# プリフライト(事前リクエスト)の設定
# 30分だけ許可
CORS_PREFLIGHT_MAX_AGE = 60 * 30
# セッション有効期間 1h
SESSION_COOKIE_AGE = 60 * 60 * 1
# 期限切れの基準を最後のページロードとする
SESSION_SAVE_EVERY_REQUEST = True

# 認証ユーザーのモデルを指定
AUTH_USER_MODEL = 'accounts.User'

LOGGING = {
    # スキーマバージョンは1固定
    'version': 1,
    # すでに作成されているロガーを無効化しないための設定
    'disable_existing_loggers': False,
    # ログの書式設定
    'formatters': {
        # 詳細ログの書式
        'verbose': {
            'format': '[%(asctime)s][pid:%(process)d][%(levelname)s] %(message)s'
        },
        # 簡易ログの書式
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        # ログレベル「CRITICAL」「ERROR」「WARNING」「INFO」「DEBUG」
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        # DBSQL
        'django.db.backends': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,

        },
        # djangoフレームワーク用のロガー
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}