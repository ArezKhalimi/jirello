from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from jirello.models import *
import logging

log = logging.getLogger('jirello')


@receiver(post_save, sender=ProjectModel)
@receiver(post_save, sender=Sprint)
@receiver(post_save, sender=Task)
def new_project(sender, created, instance, **kwargs):
    if created:
        log.info(str(sender.__name__) + ' __CREATED__: ' + str(instance))

    else:
        log.info(str(sender.__name__) + ' __CHANGE__: ' + str(instance))


@receiver(post_delete, sender=ProjectModel)
@receiver(post_save, sender=Sprint)
@receiver(post_save, sender=Task)
def book_delete(sender, instance, **kwargs):
    log.info(str(sender.__name__) + ' __DELETED__: ' + str(instance))
