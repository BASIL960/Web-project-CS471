import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "dm^e!t-1niy9k8am57&k^i_@(n)ew44p-8(wxnyvszur6@z6d6"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
ROOT_URLCONF = "libearyproject.urls"

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "apps.bookmodule.apps.BookmoduleConfig",
    # احذف usermodule إن لم تكن تستعمله
    # "apps.usermodule.apps.UsermoduleConfig",
]

# ميدل وير خفيف بدون جلسات/مصادقة/رسائل
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",     # احذفها فقط إن لم تستخدم POST
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "apps" / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.request",  # نحتاجه لـ header النشِط
            # احذف هذين لأنك أزلت auth/messages
            # "django.contrib.auth.context_processors.auth",
            # "django.contrib.messages.context_processors.messages",
        ],
    },
}]


STATIC_URL = 'static/'
STATICFILES_DIRS = [(os.path.join(BASE_DIR, "apps/static"))]
