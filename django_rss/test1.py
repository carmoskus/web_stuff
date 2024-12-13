
import os, django
os.environ["DJANGO_SETTINGS_MODULE"] = "django_rss.settings"

django.setup()

from rss_app.models import Source

