from estore.settings.base import *

DEBUG = True
STATIC_URL = "/static/"
MEDIA_URL = "http://localhost:8000/media/"

INSTALLED_APPS += ["django_extensions"]
