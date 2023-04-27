from django.db import models
from django.urls import reverse_lazy

from core.models import BaseModel


def upload_directory_file(instance, filename):
    return '{0}/{1}/{2}'.format(instance._meta.app_label, instance._meta.model_name, filename)


class TypeOfLeave(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=50)
    days = models.IntegerField(verbose_name="Jours")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Type de congé"


class Leave(BaseModel):
    type_of = models.ForeignKey(TypeOfLeave, verbose_name="Type de congé", null=True, on_delete=models.SET_NULL,
                                default=None)

    start_period = models.DateField(verbose_name="Période de départ", help_text="YYYY-MM-DD")
    end_period = models.DateField(verbose_name="Période de fin", help_text="YYYY-MM-DD")

    reason = models.TextField(verbose_name="Raison", default="-")
    observation = models.TextField(verbose_name="Observation", default="-")
    document = models.FileField(verbose_name="Document", upload_to=upload_directory_file, blank=True, null=True,
                                default=None)

    conf = {
        'icon': 'calendar',
        'description': 'value',
        'entry': reverse_lazy('core:list', kwargs={'app': 'leave', 'model': 'leave'}),
        'list': {
            'display': [('type_of', 'Type de congé'), ('created_by', 'Agent'), ('start_period', 'Période de départ'),
                        ('end_period', 'Période de fin'), ('updated', 'Mis à jour le')],
            'filter': ['type_of'],
            'action': [{
                'method': 'GET',
                'href': reverse_lazy('core:create', kwargs={'app': 'leave', 'model': 'leave'}),
                'class': 'btn btn-primary',
                'title': 'Ajouter'
            }]
        },
        'change': {
            'form': {
                'fields': ['type_of', 'start_period', 'end_period', 'document', 'reason', 'observation'],
                'inlines': []
            },
            'action': [{
                'method': 'GET',
                'href': reverse_lazy('core:delete', kwargs={'app': 'leave', 'model': 'leave'}),
                'class': 'btn btn-danger',
                'title': 'Delete',
                'condition': 'True'
            }, {
                'method': 'GET',
                'href': reverse_lazy('core:document',
                                     kwargs={'app': 'leave', 'model': 'leave', 'document': 'leave'}),
                'class': 'btn btn-info',
                'title': 'Document',
                'condition': 'obj.approved()'
            }, {
                'method': 'POST',
                'href': reverse_lazy('core:action', kwargs={'app': 'leave', 'model': 'leave', 'action': 'Approver'}),
                'class': 'btn btn-warning',
                'title': 'Approver',
                'condition': 'request.user.employee in obj.approvers() and request.user.employee not in '
                             'obj.approvals',
                'statement': 'obj.approve(request)'
            }]
        },
        'create': {
            'form': {
                'fields': ['type_of', 'start_period', 'end_period', 'document', 'reason', 'observation'],
                'inlines': []
            }
        }
    }

    def __str__(self):
        return f"Congé de {self.employee} du {self.start_period} au {self.end_period}"

    class Meta:
        verbose_name = "Congé"
