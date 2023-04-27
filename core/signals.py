from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

from django.conf import settings


@receiver(post_save, sender=apps.get_model('core', model_name='user'))
def create_user_profile(sender, instance, created, **kwargs):
    if not created: return
    instance.set_password(settings.DEFAULT_PASSWORD)
    instance.save()
