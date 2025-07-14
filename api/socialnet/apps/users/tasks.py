from celery import shared_task
import time


@shared_task
def test_celery_task():
    time.sleep(5)
    print("✅ Celery task executed successfully!")
    return "Done"
