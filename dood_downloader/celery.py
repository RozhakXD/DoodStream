import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dood_downloader.settings')

app = Celery('dood_downloader')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()