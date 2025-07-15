from django.conf import settings
from django.utils.module_loading import import_string


def get_image_storage():
    cls = import_string(settings.IMAGE_STORAGE_CLASS)
    return cls(**settings.IMAGE_STORAGE_OPTIONS)


def get_thumbnail_generator():
    cls = import_string(settings.THUMBNAIL_GENERATOR_CLASS)
    return cls(**settings.THUMBNAIL_GENERATOR_OPTIONS)
