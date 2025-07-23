import dj_database_url

from pathlib import Path
from environ import Env
env=Env()
Env.read_env()

ENVIRONMENT = env('ENVIRONMENT',default="production")

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('SECRET_KEY')

if ENVIRONMENT == 'development':
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
  'jazzmin',
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django.contrib.humanize', 
	'cloudinary_storage',
	'cloudinary',
	'django.contrib.sites',
  'widget_tweaks',
  'crispy_forms',
  'users',
  'yfcases',
  'import_export',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'whitenoise.middleware.WhiteNoiseMiddleware',
]

AUTH_USER_MODEL = 'users.CustomUser'
ROOT_URLCONF = 'src.urls'

LOGIN_URL='/login/'
LOGIN_REDIRECT_URL = 'yfcase:home'
LOGOUT_REDIRECT_URL = 'yfcase:home'

SITE_ID = 1

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'src.wsgi.application'

if ENVIRONMENT == 'development':
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': BASE_DIR / 'db.sqlite3',
		}
	}
else:
	DATABASES = {
		'default': dj_database_url.parse(env('DATABASE_URL'))
	}


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

LANGUAGE_CODE = 'zh-hant'
TIME_ZONE = 'Asia/Taipei'
USE_I18N = True
USE_L10N = True
USE_TZ = True
IMPORT_EXPORT_USE_TRANSACTIONS = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [ BASE_DIR / 'yfcases/static' ]
STATIC_ROOT=BASE_DIR /'static_cdn'

if ENVIRONMENT == 'development':
    MEDIA_ROOT = BASE_DIR / 'media' 
else:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    CLOUDINARY_STORAGE={
        'CLOUDINARY_URL': env('CLOUDINARY_URL')
    }

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER=env('EMAIL_ADDRESS')
EMAIL_HOST_PASSWORD=env('EMAIL_HOST_PASSWORD')
EMAIL_PORT=587
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=f"Django App Name {env('EMAIL_ADDRESS')}"
ACCOUNT_EMAIL_SUBJECT_PREFIX=''

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True

JAZZMIN_SETTINGS = {
	'site_title': '揚富的資料庫',
	'site_header': 'Hello World',
	'site_brand': 'I am brand',
	'welcome_sign': '歡迎來到揚富的資料庫',
	'copyright': 'yangfu1070123@gmail.com',
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
