import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "dm^e!t-1niy9k8am57&k^i_@(n)ew44p-8(wxnyvszur6@z6d6"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
ROOT_URLCONF = "libearyproject.urls"

INSTALLED_APPS = [
    # Core Django Framework Apps - NO DUPLICATES ALLOWED HERE
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",  # <-- Must be only ONE entry
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Your Project Apps
    "apps.bookmodule.apps.BookmoduleConfig",
    # "apps.usermodule.apps.UsermoduleConfig",
]

# ميدل وير خفيف بدون جلسات/مصادقة/رسائل
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",  # Re-added
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware", # Re-added
    "django.contrib.messages.middleware.MessageMiddleware",  # Re-added
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "apps" / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",  # Ensure this is here
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",      # <-- MUST be restored
            "django.contrib.messages.context_processors.messages", # <-- MUST be restored
        ],
    },
}]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
STATIC_URL = 'static/'
STATICFILES_DIRS = [(os.path.join(BASE_DIR, "apps/static"))]
