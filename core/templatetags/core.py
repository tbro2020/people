from random import randint
from django import template
from django.apps import apps
from urllib import parse

register = template.Library()


@register.filter(name='menu')
def menu(request):
    app = dict()
    for model in apps.get_models():
        meta = model._meta
        if meta.app_label in ["admin"]: continue
        if meta.model_name not in ["notification", "announcement", "employee", "leave", "exit", "requisition", "fundrequest"]: continue
        if meta.app_label not in app: app[meta.app_label] = []
        if request.user.has_perm(f"{meta.app_label}.view_{meta.model_name}"):
            app[meta.app_label].append({
                "icon": getattr(model, 'conf', {}).get('icon', None),
                "name": meta.model_name, "verbose": meta.verbose_name,
                "url": getattr(model, 'conf', {}).get('entry', None),
                "badge": model.objects.filter(target=request.user.employee, visited=False).count() if meta.model_name == "notification" else None
            })
    return {k: v for k, v in app.items() if v}


@register.filter(name='getattr')
def getter(obj, field):
    return getattr(obj, field, None)


@register.filter(name='getitem')
def getitem(obj, key):
    return obj.get(key, None)


@register.filter(name="indexOf")
def indexOf(_list, i):
    return _list.index(i)


@register.filter(name="badgeStatus")
def badgeStatus(obj, status):
    return {
        "paid": "success",
        "unpaid": "warning",
        "partial": "primary"
    }.get(getattr(obj, status))


@register.filter(name="urlparse")
def urlparse(value):
    return parse.urlencode(value)


@register.filter(name="approvers")
def approvers(model):
    return apps.get_model('core', model_name='approver').objects.filter(model=model)


@register.filter(name="background")
def background(prefix):
    backgrounds = ['primary', 'success', 'info', 'warning', 'danger']
    return f'{prefix}{backgrounds[randint(0, len(backgrounds) - 1)]}'


@register.filter(name="stack")
def stack(a, b):
    return a, b


@register.filter(name="eval")
def _eval(value, statement):
    request, obj = value
    return eval(statement)
