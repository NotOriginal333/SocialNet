from celery import shared_task

from django.apps import apps

import logging

from .services import get_thumbnail_generator

logger = logging.getLogger(__name__)


def _generate_thumbnail(model_name, image_id):
    Model = apps.get_model('images', model_name)
    try:
        image = Model.objects.get(id=image_id)
    except Model.DoesNotExist:
        logger.error(f"{model_name} with id={image_id} does not exist")
        return

    generator = get_thumbnail_generator()
    thumbnail_path = generator.generate(image.image_url)

    image.thumbnail_url = thumbnail_path
    image.save()
    logger.info(f"Thumbnail generated for {model_name} id={image_id}")


@shared_task(name="images.generate_thumbnail_for_userimage")
def generate_thumbnail_for_userimage(userimage_id):
    _generate_thumbnail('UserImage', userimage_id)


@shared_task(name="images.generate_thumbnail_for_postimage")
def generate_thumbnail_for_postimage(postimage_id):
    _generate_thumbnail('PostImage', postimage_id)
