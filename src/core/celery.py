import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
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
    },
    'send amazon review reminder emails': {
        'task': 'orders.tasks.SendAmazonReviewReminderTask',
        'schedule': crontab(hour=10, minute=0),
    },
}
