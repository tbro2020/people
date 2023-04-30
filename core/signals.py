from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

from django.conf import settings


@receiver(post_save, sender=apps.get_model('core', model_name='user'))
def post_save_user(sender, instance, created, **kwargs):
    if not created: return
    instance.set_password(settings.DEFAULT_PASSWORD)
    instance.save()


@receiver(post_save, sender=apps.get_model('core', model_name='announcement'))
def post_save_announcement(sender, instance, created, **kwargs):
    if not created: return
    instance.notify.delay()
