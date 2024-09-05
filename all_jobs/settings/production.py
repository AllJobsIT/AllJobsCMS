try:
    from .base import *
except ImportError:
    pass

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-e^9g)t7o=djaaz9g*)vmy1pivnzqc%-i_a&)_j9165n++$152("

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]