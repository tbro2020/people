from django.db import models
from django.urls import reverse_lazy
from core.models import BaseModel


class Requisition(BaseModel):
    name = models.CharField(verbose_name='Nom', max_length=150)

    conf = {
        'icon': 'shopping-cart',
        'description': 'value',
        'entry': reverse_lazy('core:list', kwargs={'app': 'logistic', 'model': 'requisition'}),
        'list': {
            'display': [('created_by', 'Agent'), ('name', 'Nom'), ('updated', 'Mis à jour le')],
            'filter': ['created'],
            'action': [{
                'method': 'GET',
                'href': reverse_lazy('core:create', kwargs={'app': 'logistic', 'model': 'requisition'}),
                'class': 'btn btn-primary',
                'title': 'Ajouter'
            }]
        },
        'change': {
            'form': {
                'fields': ['name'],
                'inlines': [{
                    'app': 'logistic',
                    'model': 'product'
                }]
            },
            'action': [{
                'method': 'GET',
                'href': reverse_lazy('core:delete', kwargs={'app': 'logistic', 'model': 'requisition'}),
                'class': 'btn btn-danger',
                'title': 'Delete'
            }, {
                'method': 'GET',
                'href': reverse_lazy('core:document',
                                     kwargs={'app': 'logistic', 'model': 'requisition', 'document': 'requisition'}),
                'class': 'btn btn-info',
                'title': 'Document'
            }]
        },
        'create': {
            'form': {
                'fields': ['name'],
                'inlines': []
            }
        }
    }

    def __str__(self):
        return f'{self.name}'

    def products(self):
        return Product.objects.filter(requisition=self)

    class Meta:
        verbose_name = 'Requisition'


class Product(models.Model):
    requisition = models.ForeignKey(Requisition, null=True, on_delete=models.SET_NULL, default=None)

    name = models.CharField(verbose_name='Nom', max_length=150)
    quantity = models.FloatField(verbose_name='Quantite', default=0.0)
    unit = models.CharField(verbose_name='Unite', max_length=10)

    updated = models.DateTimeField(verbose_name="Mise à jour le", auto_now=True)
    created = models.DateTimeField(verbose_name="Créée le", auto_now_add=True)

    def __str__(self):
        return f'{self.name}/{self.quantity}'

    class Meta:
        verbose_name = 'Produit'
