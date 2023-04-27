from django.db import models
from django.urls import reverse_lazy

from core.models import BaseModel


def upload_directory_file(instance, filename):
    return '{0}/{1}/{2}'.format(instance._meta.app_label, instance._meta.model_name, filename)


class FundRequest(BaseModel):
    CURRENCIES = (
        ('CDF', 'CDF'),
        ('USD', 'USD')
    )

    description = models.TextField(verbose_name='Description', default='-')
    doc = models.FileField(verbose_name='Document', upload_to=upload_directory_file, blank=True, null=True, default=None)

    currency = models.CharField(verbose_name='Devise', max_length=25, choices=CURRENCIES, default=CURRENCIES[0][0])
    amount = models.DecimalField(verbose_name='Montant', max_digits=5, decimal_places=2)

    conf = {
        'icon': 'dollar-sign',
        'description': 'value',
        'entry': reverse_lazy('core:list', kwargs={'app': 'social', 'model': 'fundrequest'}),
        'list': {
            'display': [('description', 'Description'), ('currency', 'Device'), ('amount', 'Montant'), ('updated', 'Mis à jour le')],
            'filter': [],
            'action': [{
                'method': 'GET',
                'href': reverse_lazy('core:create', kwargs={'app': 'social', 'model': 'fundrequest'}),
                'class': 'btn btn-primary',
                'title': 'Ajouter'
            }]
        },
        'change': {
            'form': {
                'fields': ['doc', 'currency', 'amount', 'description'],
                'inlines': []
            },
            'action': [{
                'method': 'GET',
                'href': reverse_lazy('core:delete', kwargs={'app': 'social', 'model': 'fundrequest'}),
                'class': 'btn btn-danger',
                'title': 'Delete',
                'condition': 'True'
            }, {
                'method': 'GET',
                'href': reverse_lazy('core:document',
                                     kwargs={'app': 'social', 'model': 'fundrequest', 'document': 'fundrequest'}),
                'class': 'btn btn-info',
                'title': 'Document',
                'condition': 'obj.approved()'
            }, {
                'method': 'POST',
                'href': reverse_lazy('core:action', kwargs={'app': 'social', 'model': 'fundrequest', 'action': 'Approver'}),
                'class': 'btn btn-warning',
                'title': 'Approver',
                'condition': 'request.user.employee in obj.approvers() and request.user.employee not in '
                             'obj.approvals',
                'statement': 'obj.approve(request)'
            }]
        },
        'create': {
            'form': {
                'fields': ['doc', 'currency', 'amount', 'description'],
                'inlines': []
            }
        }
    }
