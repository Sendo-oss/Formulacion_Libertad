from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def get_env(name, default=None):
    return os.getenv(name, default)


def get_env_bool(name, default=False):
    value = get_env(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def get_env_list(name, default=""):
    value = get_env(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


DEBUG = get_env_bool("DEBUG", True)

SECRET_KEY = get_env("SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "dev-secret-key-change-me"
    else:
        raise ImproperlyConfigured("Debes definir SECRET_KEY en el archivo .env para ejecutar con DEBUG=False.")

ALLOWED_HOSTS = get_env_list("ALLOWED_HOSTS", "127.0.0.1,localhost")
CSRF_TRUSTED_ORIGINS = get_env_list("CSRF_TRUSTED_ORIGINS", "")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.usuarios",
    "apps.inventario",
    "apps.formulaciones",
    "apps.alertas",
    "apps.dashboard",
    "apps.calculadora",
    "apps.documentacion",
    "apps.noticias",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "apps.usuarios.middleware.ForzarCambioContrasenaMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DB_ENGINE = get_env("DB_ENGINE", "postgresql").lower()

if DB_ENGINE == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / get_env("SQLITE_NAME", "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": get_env("DB_NAME", "formulacion_magistral_db"),
            "USER": get_env("DB_USER", "postgres"),
            "PASSWORD": get_env("DB_PASSWORD", "intesud"),
            "HOST": get_env("DB_HOST", "127.0.0.1"),
            "PORT": get_env("DB_PORT", "5432"),
        }
    }

AUTH_USER_MODEL = "usuarios.Usuario"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "/login/"

LANGUAGE_CODE = "es-ec"
TIME_ZONE = "America/Guayaquil"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "dashboard:inicio"
LOGOUT_REDIRECT_URL = "login"

EMAIL_BACKEND = get_env("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = get_env("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(get_env("EMAIL_PORT", "587"))
EMAIL_HOST_USER = get_env("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = get_env("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = get_env_bool("EMAIL_USE_TLS", True)
EMAIL_USE_SSL = get_env_bool("EMAIL_USE_SSL", False)
DEFAULT_FROM_EMAIL = get_env("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER or "no-reply@itslibertad.edu.ec")

SECURE_SSL_REDIRECT = get_env_bool("SECURE_SSL_REDIRECT", False)
SESSION_COOKIE_SECURE = get_env_bool("SESSION_COOKIE_SECURE", not DEBUG)
CSRF_COOKIE_SECURE = get_env_bool("CSRF_COOKIE_SECURE", not DEBUG)
SECURE_HSTS_SECONDS = int(get_env("SECURE_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = get_env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", False)
SECURE_HSTS_PRELOAD = get_env_bool("SECURE_HSTS_PRELOAD", False)
SECURE_CONTENT_TYPE_NOSNIFF = get_env_bool("SECURE_CONTENT_TYPE_NOSNIFF", True)
SECURE_REFERRER_POLICY = get_env("SECURE_REFERRER_POLICY", "same-origin")
X_FRAME_OPTIONS = get_env("X_FRAME_OPTIONS", "DENY")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") if get_env_bool("USE_X_FORWARDED_PROTO", False) else None
