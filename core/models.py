import time
from datetime import date

import requests
from celery import shared_task
from django.conf import settings
from django.urls import reverse_lazy
from django.apps import apps
from django.db import models

from django.contrib.auth.models import AbstractUser
from core.managers import UserManager
from django.contrib import messages

from django_currentuser.db.models import CurrentUserField
from functools import reduce
import operator


def upload_directory_file(instance, filename):
    return '{0}/{1}/{2}'.format(instance._meta.app_label, instance._meta.model_name, filename)


def MODEL_CHOICES():
    data = [('exit.exit', 'Approbation sur la sortie'), ('leave.leave', 'Approbation sur le congé'),
            ('logistic.requisition', 'Approbation sur requisition'),
            ('social.fundrequest', 'Approbation sur demande de fonds')]
    return data


class User(AbstractUser):
    employee = models.OneToOneField('employee.Employee', null=True, on_delete=models.SET_NULL, default=None)
    email = models.EmailField(unique=True, db_index=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.employee:
            return f"{self.employee}"
        return f"{self.email}"


class Announcement(models.Model):
    title = models.CharField(verbose_name="Titre", max_length=50)
    description = models.TextField(verbose_name="Description")
    doc = models.FileField(verbose_name="Document", upload_to=upload_directory_file)
    broadcast = models.BooleanField(default=False, verbose_name="Diffusé", help_text="Diffuser cette annonce à tous "
                                                                                     "les agents actifs par le biais "
                                                                                     "de différents canaux.")
    branches = models.ManyToManyField('employee.Branch', verbose_name="Branche", blank=True)
    updated = models.DateTimeField(verbose_name="Mise à jour le", auto_now=True)
    created = models.DateTimeField(verbose_name="Créée le", auto_now_add=True)

    conf = {
        'icon': 'mic',
        'entry': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'announcement'}),
        'list': {
            'display': [('title', 'Titre'), ('broadcast', 'Diffuser'), ('updated', 'Mis à jour le')],
            'filter': [],
            'action': [{
                'method': 'GET',
                'href': reverse_lazy('core:create', kwargs={'app': 'core', 'model': 'announcement'}),
                'class': 'btn btn-primary',
                'title': 'Ajouter'
            }]
        },
        'create': {
            'form': {
                'fields': ['title', 'doc', 'broadcast', 'description', 'branch'],
                'inlines': []
            }
        }
    }

    def __str__(self):
        return f"{self.title}"

    @shared_task
    def notify(self):
        if not self.broadcast or not settings.TG_TOKEN: return
        branches = self.branches.all().values_list('name', flat=True)

        if not branches: return
        employees = apps.get_model('core', model_name='employee').objects.filter(branch__in=branches, status='actif')

        TG_API_URL = f'https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage'
        [requests.post(TG_API_URL, json={'chat_id': employee.tg.last_chat_id, 'text': self.description}) for employee in employees]

    class Meta:
        verbose_name = "Annonce"


class Notification(models.Model):
    message = models.TextField(verbose_name="Message")
    target = models.ForeignKey('employee.Employee', verbose_name="Cible", null=True, on_delete=models.SET_NULL)

    redirect_to = models.URLField(verbose_name="Rediriger vers", max_length=250)
    visited = models.BooleanField(verbose_name="Visité", default=False)

    updated = models.DateTimeField(verbose_name="Mise à jour le", auto_now=True)
    created = models.DateTimeField(verbose_name="Créée le", auto_now_add=True)

    def __str__(self):
        return f"{self.message}"

    conf = {
        'icon': 'bell',
        'entry': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'notification'}),
        'list': {
            'display': [('message', 'Message'), ('target', 'Cible'), ('visited', 'Visité'),
                        ('updated', 'Mis à jour le')],
            'filter': ['visited'],
            'action': []
        }
    }

    class Meta:
        verbose_name = "Notification"


class Approver(models.Model):
    model = models.CharField(verbose_name='Model', max_length=30, choices=MODEL_CHOICES())
    employee = models.ForeignKey('employee.Employee', verbose_name='Employee', null=True, on_delete=models.SET_NULL)

    updated = models.DateTimeField(verbose_name="Mise à jour le", auto_now=True)
    created = models.DateTimeField(verbose_name="Créée le", auto_now_add=True)

    def __str__(self):
        return f'{self.model}/{self.employee}'

    class Meta:
        verbose_name = 'Approbateur'
        unique_together = ('model', 'employee',)


class Approval(models.Model):
    model = models.CharField(verbose_name='Model', max_length=30, choices=MODEL_CHOICES())
    _pk = models.IntegerField(verbose_name='Identifiant unique')

    approved_by = models.ForeignKey('employee.Employee', verbose_name='Employee', null=True, on_delete=models.SET_NULL)

    updated = models.DateTimeField(verbose_name="Mise à jour le", auto_now=True)
    created = models.DateTimeField(verbose_name="Créée le", auto_now_add=True)

    def __str__(self):
        return f'Obj {self.model} #{self.pk} approved by {self.approved_by}'

    class Meta:
        verbose_name = 'Approbation'


class BaseModel(models.Model):
    created_by = CurrentUserField(verbose_name="Créée par")
    updated = models.DateTimeField(verbose_name="Mise à jour le", auto_now=True)
    created = models.DateTimeField(verbose_name="Créée le", auto_now_add=True)

    def approvers(self):
        app_label, model_name = self._meta.app_label, self._meta.model_name
        user = self.created_by

        data = {'employee__branch': getattr(user.employee, 'branch', None), 'employee__direction': getattr(user.employee, 'direction', None),
                'employee__subDirection': getattr(user.employee, 'subDirection', None), 'employee__service': getattr(user.employee, 'service', None)}
        data = {key: value for key, value in data.items() if value}

        qs = Approver.objects.select_related().filter(model=f'{app_label}.{model_name}')
        if data: qs = qs.filter(reduce(operator.or_, (models.Q(**d) for d in (dict([i]) for i in data.items())))).values_list('employee', flat=True)
        return apps.get_model('employee', model_name='employee').objects.filter(id__in=qs)

    @property
    def approvals(self):
        app_label, model_name = self._meta.app_label, self._meta.model_name
        qs = Approval.objects.select_related().filter(model=f'{app_label}.{model_name}', _pk=self.pk).values_list(
            'approved_by', flat=True)
        return apps.get_model('employee', model_name='employee').objects.filter(id__in=qs)

    def approved(self):
        approvers = self.approvers().count()
        return approvers == self.approvals.count()

    def approve(self, request):
        app_label, model_name = self._meta.app_label, self._meta.model_name
        obj, created = Approval.objects.get_or_create(
            **{'model': f'{app_label}.{model_name}', '_pk': self.pk, 'approved_by': request.user.employee})
        if not created: return False
        messages.add_message(request, level=messages.SUCCESS,
                             message=f'{self._meta.verbose_name} #{self.id} has been approved')
        return True

    class Meta:
        abstract = True


class Event:
    def __init__(self):
        self.today = date.today()
        self.leaves = apps.get_model('leave', model_name='leave')
        self.employee = apps.get_model('employee', model_name='employee')

    def get_leaves(self):
        leaves = self.leaves.objects.select_related().filter(created__year=self.today.year)
        return [{
            'id': f'leave-{leave.id}',
            'name': f'{leave.type_of.name}',
            'type': 'event',
            'date': [leave.start_period, leave.end_period],
            'description': f'{leave.created_by.employee} {leave.reason}'
        } for leave in leaves if leave.approved()]

    def get_birthdays(self):
        employees = self.employee.objects.select_related().filter(status='actif')
        return [{
            'id': f'birthday-{employee.id}',
            'name': f'Birthday of {employee.full_name()}',
            'type': 'birthday',
            'date': employee.dob,
            'description': f'{employee} of {employee.direction.name}'
        } for employee in employees]

    def all(self):
        return self.get_leaves() + self.get_birthdays()
