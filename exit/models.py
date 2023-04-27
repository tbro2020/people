from django.db import models
from django.urls import reverse_lazy

from core.models import BaseModel


class Exit(BaseModel):
    exit_time = models.TimeField(verbose_name='Heure de sortie', help_text="HH:MM:SS")
    reason = models.TextField(verbose_name='Motif de sortie')
    destination = models.CharField(verbose_name='Destination', max_length=250)
    return_time = models.TimeField(verbose_name='Heure de retour', help_text="HH:MM:SS")
    observation = models.TextField(verbose_name='Observation')

    conf = {
        'icon': 'log-out',
        'description': 'value',
        'entry': reverse_lazy('core:list', kwargs={'app': 'exit', 'model': 'exit'}),
        'list': {
            'display': [('created_by', 'Agent'), ('exit_time', 'Heure de sortie'), ('reason', 'Motif de sortie'), ('destination', 'Destination'),
                        ('return_time', 'Heure de retour'), ('updated', 'Mis à jour le')],
            'filter': [],
            'action': [{
                'method': 'GET',
                'href': reverse_lazy('core:create', kwargs={'app': 'exit', 'model': 'exit'}),
                'class': 'btn btn-primary',
                'title': 'Ajouter'
            }]
        },
        'change': {
            'form': {
                'fields': ['exit_time', 'reason', 'destination', 'return_time', 'observation'],
                'inlines': []
            },
            'action': [{
                'method': 'GET',
                'href': reverse_lazy('core:delete', kwargs={'app': 'exit', 'model': 'exit'}),
                'class': 'btn btn-danger',
                'title': 'Delete'
            }, {
                'method': 'GET',
                'href': reverse_lazy('core:document',
                                     kwargs={'app': 'exit', 'model': 'exit', 'document': 'exit'}),
                'class': 'btn btn-info',
                'title': 'Document'
            }]
        },
        'create': {
            'form': {
                'fields': ['exit_time', 'reason', 'destination', 'return_time', 'observation'],
                'inlines': []
            }
        }
    }

    def __str__(self):
        return f'Autorisation de sortie de {self.created_by}'

    class Meta:
        verbose_name = 'Bon de sortie'
