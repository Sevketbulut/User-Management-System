from pathlib import Path
from datetime import timedelta
import os
import firebase_admin
from firebase_admin import credentials, firestore, storage

# -------------------------------------------------
# BASE SETTINGS
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-)b!y4+sg2dfuyav4^+963=!bescg!*l^tbryaig8@9-jb00=z9'
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '.ngrok.io',
    '.ngrok-free.dev',
]

# -------------------------------------------------
# APPS
# -------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'django_filters',
    'rest_framework_simplejwt',

    # Local apps
    'users.apps.UsersConfig', #Kendi users modelimizi kullanıyoruz
]
AUTH_USER_MODEL = 'users.User'

# -------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------
MIDDLEWARE = [ #Gelen/giden isteklere müdahale
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'UserManagementSystem_backend.urls' #URL yönlendirmesi

TEMPLATES = [ #Şablonun render edilişi
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'UserManagementSystem_backend.wsgi.application'

# -------------------------------------------------
# DATABASE
# -------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -------------------------------------------------
# PASSWORD VALIDATORS
# -------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [ #kullanıcı şifre güvenliği
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------------------------
# LANGUAGE & TIMEZONE
# -------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -------------------------------------------------
# STATIC & MEDIA FILES
# -------------------------------------------------
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------
# REST FRAMEWORK & JWT CONFIG
# -------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# -------------------------------------------------
# CUSTOM AUTHENTICATION (email login)
# -------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'users.auth_backend.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# -------------------------------------------------
# FIREBASE CONFIGURATION (Firestore + GCS)
# -------------------------------------------------
FIREBASE_KEY_PATH = BASE_DIR / "firebase-admin-key.json"

if os.path.exists(FIREBASE_KEY_PATH):
    try:
        # Firebase App initialize
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_KEY_PATH)
            firebase_admin.initialize_app(cred, {
                'storageBucket': 'sevenapps-2befe.appspot.com'  # 🔹 BUCKET ADINI BURADA DEĞİŞTİR
            })

        # Firestore ve GCS bağlantısı
        FIRESTORE_CLIENT = firestore.client()
        STORAGE_BUCKET = storage.bucket()
        print("✅ Firebase Firestore & GCS bağlantısı başarıyla kuruldu.")

    except Exception as e:
        print(f"⚠️ Firebase başlatılamadı: {e}")
else:
    print("⚠️ firebase-admin-key.json dosyası bulunamadı, Firestore & GCS devre dışı.")
