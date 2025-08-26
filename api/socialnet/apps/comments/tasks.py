from celery import shared_task

from apps.posts.models import Post


@shared_task
def update_post_comments_count(post_id):
    try:
        post = Post.objects.get(id=post_id)
        post.comments_count = post.comments.count()
        post.save(update_fields=['comments_count'])
    except Post.DoesNotExist:
        pass
