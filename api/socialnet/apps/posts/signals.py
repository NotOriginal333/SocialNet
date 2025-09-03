from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.feed.tasks import post_created_fanout
from apps.posts.models import Post


@receiver(post_save, sender=Post)
def on_post_created(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: post_created_fanout.delay(instance.id))
