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
    'send scheduled emails': {
        'task': 'users.tasks.SendScheduledEmailsTask',
        'schedule': crontab(hour=9, minute=0),
    },
    'send amazon review reminder emails': {
        'task': 'orders.tasks.SendAmazonReviewReminderTask',
        'schedule': crontab(hour=10, minute=0),
    },
    'sync amazon orders': {
        'task': 'orders.tasks.SyncAmazonOrdersTask',
        'schedule': crontab(hour=15, minute=0),
    },
    'send weekly marketing email': {
        'task': 'reports.tasks.SendWeeklyMarketingEmailTask',
        'schedule': crontab(hour=8, minute=30, day_of_week=1),
    },
}
