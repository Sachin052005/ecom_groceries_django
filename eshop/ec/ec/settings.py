from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ifb)bxvl6f4lruchu(x6b+tvg-vjvm(8i1t+j1)o^#b0#tc!6%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ec.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ec.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

#DATABASES = {
 #   'default': {
  #      'ENGINE': 'django.db.backends.sqlite3',
   #     'NAME': BASE_DIR / 'db.sqlite3',
   # }
#}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecomm',
        'USER': 'root',
        'PASSWORD': 'Sachin123@', 
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'idpsachin@gmail.com'
EMAIL_HOST_PASSWORD = 'hxsu osok vtot qnhf'


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
LOGIN_REDIRECT_URL='/'

SATATICFILES_DIRS =[os.path.join(BASE_DIR,'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



RAZOR_KEY_ID ="rzp_test_1Uk6lMzkjxJsPy"
RAZOR_KEY_SECRET ="MNYqfSBGGkNZrf7HRKoOBBLR"



#unfold admin config

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "My Site Title",  # Default title
    "SITE_HEADER": "My Site Header",  # Default header
    "SITE_URL": "/",

    "SITE_ICON": {
        "light": lambda request: static("logo.jpg"),  # Light mode
        "dark": lambda request: static("logo.jpg"),    # Dark mode
    },
    "SITE_LOGO": {
        "light": lambda request: static("logo.jpg"),
        "dark": lambda request: static("logo.jpg"),
    },
    "SITE_SYMBOL": "speed",  
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",  
            "type": "image/svg+xml",
            "href": lambda request: static("logo.jpg"),
        },
    ],

    "SHOW_HISTORY": True, #recent action 
    "SHOW_VIEW_ON_SITE": True,#viewsite
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 266",
            "800": "197 33 168",
            "900": "88 28 135",
            "950": "59 7 108",
        },
    },
    "SIDEBAR": {
        "show_search": True, # search options
        "show_all_application": False, # applications in bottom
        "navigation": [
            {
                "title": _("Navigation Grocery"),
                "separator": True,# line between space
                "collapsible": True,#side viewer
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",#fonts.google.com
                        "link": reverse_lazy("admin:index"),
                        "badge": "Main Admin",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Product"),
                        "icon": "production_quantity_limits",#fonts.google.com
                        "link": reverse_lazy("admin:app_product_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Customer"),
                        "icon": "support_agent",#fonts.google.com
                        "link": reverse_lazy("admin:app_customer_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Cart"),
                        "icon": "shopping_cart",#fonts.google.com
                        "link": reverse_lazy("admin:app_cart_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Payment"),
                        "icon": "payments",#fonts.google.com
                        "link": reverse_lazy("admin:app_payment_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Orderplaced"),
                        "icon": "orders",#fonts.google.com
                        "link": reverse_lazy("admin:app_orderplaced_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    
                ],  
            },
        ],
    },
}

TABS = [
    {
        "models": [
            "app_label.model_name_in_lowercase",
        ],
        "items": [
            {
                "title": _("Your custom title"),
                "link": reverse_lazy("admin:app_label_model_name_changelist"),
                "permission": "sample_app.permission_callback",
            },
        ],
    },
]


# APPEND_SLASH = False