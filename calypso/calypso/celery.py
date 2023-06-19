import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calypso.settings')

app = Celery('calypso')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update instagram posts': {
        'task': 'UpdateInstagramPosts',
        'schedule': crontab(hour=0, minute=0),
    },
    'send review reminder emails': {
        'task': 'users.tasks.SendReviewReminderTask',
        'schedule': crontab(hour=9, minute=0),
    }
}
