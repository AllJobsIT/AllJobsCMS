from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-e^9g)t7o=djaaz9g*)vmy1pivnzqc%-i_a&)_j9165n++$152("

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.all_jobs.mail.backends.console.EmailBackend"

try:
    from .local import *
except ImportError:
    pass
