from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.apps import apps

models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

# ---------------------------------------------------
permission = apps.get_model('auth', 'Permission')
[permission.objects.get_or_create(**{
    'name': 'Can view all %s' % model._meta.verbose_name_plural,
    'content_type': ContentType.objects.get_for_model(model),
    'codename': 'view_all_%s' % model._meta.model_name
}) for model in apps.get_models() if model._meta.app_label in ['leave', 'exit', 'logistic']]
