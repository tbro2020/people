from django.db import models
from django.urls import reverse_lazy
from core.models import BaseModel


class Item(models.Model):
    name = models.CharField(verbose_name='Nom', max_length=150)

    conf = {
        'icon': 'shopping-cart',
        'description': 'Articles disponible',
        'entry': reverse_lazy('core:list', kwargs={'app': 'logistic', 'model': 'item'}),
        'list': {
            'display': [('name', 'Nom')],
            'action': [{
                'method': 'GET',
                'href': reverse_lazy('core:create', kwargs={'app': 'logistic', 'model': 'item'}),
                'class': 'btn btn-primary',
                'title': 'Ajouter'
            }]
        },
        'change': {
            'form': {
                'fields': ['name'],
                'inlines': []
            },
            'action': [{
                'method': 'GET',
                'href': reverse_lazy('core:delete', kwargs={'app': 'logistic', 'model': 'item'}),
                'class': 'btn btn-danger',
                'title': 'Delete',
                'condition': 'True'
            }]
        },
        'create': {
            'form': {
                'fields': ['name'],
                'inlines': []
            }
        },
    }

    def __str__(self):
        return self.name

class Requisition(BaseModel):
    name = models.CharField(verbose_name='Nom', max_length=150)

    conf = {
        'icon': 'shopping-cart',
        'description': 'Gestion des requêtes de produits',
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
                'title': 'Delete',
                'condition': 'True'
            }, {
                'method': 'GET',
                'href': reverse_lazy('core:document',
                                     kwargs={'app': 'logistic', 'model': 'requisition', 'document': 'requisition'}),
                'class': 'btn btn-info',
                'title': 'Document',
                'condition': 'obj.approved()'
            }, {
                'method': 'POST',
                'href': reverse_lazy('core:action', kwargs={'app': 'logistic', 'model': 'requisition', 'action': 'Approver'}),
                'class': 'btn btn-warning',
                'title': 'Approver',
                'condition': 'request.user.employee in obj.approvers() and request.user.employee not in '
                             'obj.approvals',
                'statement': 'obj.approve(request)'
            }]
        },
        'create': {
            'form': {
                'fields': ['name'],
                'inlines': []
            }
        },
        'read': {
            'action': [{
                'method': 'GET',
                'href': reverse_lazy('core:document',
                                     kwargs={'app': 'logistic', 'model': 'requisition', 'document': 'requisition'}),
                'class': 'btn btn-info',
                'title': 'Document',
                'condition': 'True'
            }]
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

    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    unit = models.CharField(verbose_name='Unite', max_length=10)
    quantity = models.FloatField(verbose_name='Quantite', default=0.0)

    updated = models.DateTimeField(verbose_name="Mise à jour le", auto_now=True)
    created = models.DateTimeField(verbose_name="Créée le", auto_now_add=True)

    def __str__(self):
        return f'{self.name}/{self.quantity}'

    class Meta:
        verbose_name = 'Produit'
