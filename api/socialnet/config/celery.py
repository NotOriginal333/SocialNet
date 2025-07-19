import os
from celery import Celery

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

app.autodiscover_tasks()
