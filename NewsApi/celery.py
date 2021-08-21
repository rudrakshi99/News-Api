from __future__ import absolute_import
from datetime import timezone
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsApi.settings')
app = Celery('NewsApi')

app.conf.beat_schedule = {
    'add-every-1-hour': {
        'task': 'Api.tasks.task_news_update',
        'schedule': crontab(hour=1, minute=0),
    }
}

app.conf.update(timezone = 'Asia/Kolkata')
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))