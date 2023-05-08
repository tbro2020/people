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
[[permission.objects.get_or_create(**{
    'name': 'Can view all %s in %s' % (model._meta.model_name, el),
    'content_type': ContentType.objects.get_for_model(model),
    'codename': f'view_all_{model._meta.model_name}_in_{el}'
}) for el in ['branch', 'direction', 'subDirection', 'service']] for model in apps.get_models() if
 model._meta.app_label in ['leave', 'exit', 'logistic', 'social']]
