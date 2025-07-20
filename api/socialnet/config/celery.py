import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_queues = {
    'media': {
        'exchange': 'media',
        'routing_key': 'media',
    },
    'follows': {
        'exchange': 'follows',
        'routing_key': 'follows',
    }
}

app.conf.task_default_queue = 'default'

app.conf.task_routes = {
    'images.*': {'queue': 'media'},
    'apps.follows.tasks.*': {'queue': 'follows'},
}

app.conf.beat_schedule = {
    'generate-follow-recommendations-every-day': {
        'task': 'apps.follows.tasks.update_recommendations_for_user',
        'schedule': crontab(hour=3, minute=0),  # every day at 3 a.m.
    },
}

app.autodiscover_tasks()
