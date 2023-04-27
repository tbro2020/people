from django.db.models import Q
from django import forms
import django_filters

from functools import reduce
import operator


class AdvanceFilterSet(django_filters.FilterSet):
    q = django_filters.CharFilter("", method='search', label='', widget=forms.TextInput(attrs={'class': 'd-none'}))

    def search(self, queryset, name, value):
        _q = {f"{field}__icontains": value for field in [field.name for field in self._meta.model._meta.fields if field.get_internal_type() == 'CharField']}
        return queryset.filter(reduce(operator.or_, (Q(**d) for d in (dict([i]) for i in _q.items()))))


def filterset_factory(model, filter="__all__"):
    meta = type(str("Meta"), (object,), {"model": model, "fields": filter})
    filterset = type(str("%sFilterSet" % model._meta.object_name), (AdvanceFilterSet,), {"Meta": meta})
    return filterset
