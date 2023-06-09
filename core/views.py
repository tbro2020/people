from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.apps import apps

from django.forms import modelform_factory, inlineformset_factory
from core.forms import AcceptForm, Row3Form, InlineForm
from core.filters import filterset_factory
from core.models import Event

Notification = apps.get_model('core', model_name='notification')
Announcement = apps.get_model('core', model_name='announcement')


class Home(LoginRequiredMixin, View):
    def get(self, request):
        cards = {model._meta.verbose_name_plural: model.objects.all().count() for model in apps.get_models() if model._meta.app_label in ['employee', 'leave', 'exit', 'logistic', 'social']}
        if not hasattr(request.user.employee, 'branch'):
            return render(request, f'{self.__class__.__name__.lower()}.html', locals())

        branch = request.user.employee.branch
        notifications = Notification.objects.filter(target=request.user.employee, visited=False)[:6]
        items = Announcement.objects.filter(branches__name=branch)[:6]
        return render(request, f'{self.__class__.__name__.lower()}.html', locals())


class Read(LoginRequiredMixin, View):
    def get(self, request, app, model):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, **request.GET.dict())

        if hasattr(obj, 'redirect_to'):
            if hasattr(obj, 'visited'):
                setattr(obj, 'visited', True)
                obj.save()
            return HttpResponseRedirect(getattr(obj, 'redirect_to'))

        inlines = []
        for inline in getattr(model, 'conf', {}).get('change', {}).get('form', {}).get('inlines', []):
            _model = apps.get_model(inline.get('app'), model_name=inline.get('model'))
            inlines.append(_model.objects.filter(**{model._meta.model_name: obj}))
        return render(request, f'{self.__class__.__name__.lower()}.html', locals())


class List(LoginRequiredMixin, View):
    def get(self, request, app, model):
        model = apps.get_model(app, model_name=model)

        query = {}
        fields = {'filter': getattr(model, 'conf', {}).get('list', {}).get('filter', [])}

        if 'created_by' in [field.name for field in model._meta.get_fields()]:
            query = {
                'created_by__employee__branch': request.user.employee.branch,
                'created_by__employee__direction': request.user.employee.direction,
                'created_by__employee__subDirection': request.user.employee.subDirection,
                'created_by__employee__service': request.user.employee.service
            }
            query = {k: v for k, v in query.items() if v is not None}
            if len(query) == 4: query['created_by'] = request.user

        _query = query.copy()
        for key, value in _query.items():
            if request.user.has_perm(f'{app}.view_all_{model._meta.model_name}_in_{key.split("__")[-1]}') and key in query:
                query.pop(key, None)
                query.pop('created_by', None)

        qs = model.objects.select_related().filter(**query)
        _filter = filterset_factory(model, **fields)(request.GET, queryset=qs)
        filter_form = _filter.form
        qs = _filter.qs

        qs = Paginator(qs, 25)
        qs = qs.page(request.GET.get('page', 1))

        return render(request, f'{self.__class__.__name__.lower()}.html', locals())


class Create(LoginRequiredMixin, View):
    def get(self, request, app, model):
        model = apps.get_model(app, model_name=model)

        inlines = []
        fields = getattr(model, 'conf', {}).get('create', {}).get('form', {}).get('fields', '__all__')
        form = modelform_factory(model, fields=fields, form=Row3Form)()

        for inline in getattr(model, 'conf', {}).get('create', {}).get('form', {}).get('inlines', []):
            _fields = inline.get('fields', '__all__')
            _model = apps.get_model(inline.get('app'), model_name=inline.get('model'))
            _form = inlineformset_factory(model, _model, form=InlineForm, fields=_fields, extra=1)()
            inlines.append(_form)
        return render(request, f'{self.__class__.__name__.lower()}.html', locals())

    def post(self, request, app, model):
        model = apps.get_model(app, model_name=model)

        inlines = []
        fields = getattr(model, 'conf', {}).get('create', {}).get('form', {}).get('fields', '__all__')
        form = modelform_factory(model, fields=fields, form=Row3Form)(request.POST or None, request.FILES or None)

        for inline in getattr(model, 'conf', {}).get('create', {}).get('form', {}).get('inlines', []):
            _fields = inline.get('fields', '__all__')
            _model = apps.get_model(inline.get('app'), model_name=inline.get('model'))
            _form = inlineformset_factory(model, _model, form=InlineForm, fields=_fields, extra=1)(request.POST or None,
                                                                                                   request.FILES or None)
            inlines.append(_form)

        if not form.is_valid() or False in [inline.is_valid() for inline in inlines]:
            for error in form.errors: messages.add_message(request, messages.ERROR, message=error)
            return render(request, f'{self.__class__.__name__.lower()}.html', locals())

        form.save()
        [inline.save() for inline in inlines]
        messages.add_message(request, messages.SUCCESS,
                             message=f'The {model._meta.verbose_name} has been successfuly created')

        # Notification need to be thread action
        approvers = getattr(form.instance, 'approvers', [])
        if not isinstance(approvers, list): approvers = approvers()

        approvers = [Notification(**{
            'message': f'{model._meta.verbose_name} #{form.instance.id} approval required',
            'target_id': approver.id,
            'redirect_to': f"{reverse_lazy('core:change', kwargs={'app': app, 'model': model._meta.model_name})}?pk={form.instance.id}",
            'visited': False
        }) for approver in approvers]
        Notification.objects.bulk_create(approvers)

        return redirect(
            f"{reverse('core:change', kwargs={'app': app, 'model': model._meta.model_name})}?pk={form.instance.pk}")


class Change(LoginRequiredMixin, View):
    def get(self, request, app, model):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, **request.GET.dict())

        if 'change' not in getattr(model, 'conf', {}):
            return redirect(f"{reverse('core:read', kwargs={'app': app, 'model': model._meta.model_name})}?pk={obj.id}")

        if hasattr(obj, 'approved') and obj.approved() and request.user.employee not in obj.approvers():
            return redirect(f"{reverse('core:read', kwargs={'app': app, 'model': model._meta.model_name})}?pk={obj.id}")

        inlines = []
        fields = getattr(model, 'conf', {}).get('change', {}).get('form', {}).get('fields', '__all__')
        form = modelform_factory(model, fields=fields, form=Row3Form)(instance=obj)

        for inline in getattr(model, 'conf', {}).get('change', {}).get('form', {}).get('inlines', []):
            _fields = inline.get('fields', '__all__')
            _model = apps.get_model(inline.get('app'), model_name=inline.get('model'))
            _form = inlineformset_factory(model, _model, form=Row3Form, fields=_fields,
                                          exclude=(model._meta.model_name,), extra=1, can_delete=True)(instance=obj)
            inlines.append(_form)
        return render(request, f'{self.__class__.__name__.lower()}.html', locals())

    def post(self, request, app, model):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, **request.GET.dict())

        inlines = []
        fields = getattr(model, 'conf', {}).get('change', {}).get('form', {}).get('fields', '__all__')
        form = modelform_factory(model, fields=fields, form=Row3Form)(request.POST or None, request.FILES or None,
                                                                      instance=obj)

        for inline in getattr(model, 'conf', {}).get('change', {}).get('form', {}).get('inlines', []):
            _fields = inline.get('fields', '__all__')
            _model = apps.get_model(inline.get('app'), model_name=inline.get('model'))
            _form = inlineformset_factory(model, _model, form=InlineForm, fields=_fields, extra=1)(request.POST or None,
                                                                                                   request.FILES or None,
                                                                                                   instance=obj)
            inlines.append(_form)

        if not form.is_valid() or False in [inline.is_valid() for inline in inlines]:
            for error in form.errors: messages.add_message(request, messages.ERROR, message=error.as_text())
            return render(request, f'{self.__class__.__name__.lower()}.html', locals())

        form.save()
        [inline.save() for inline in inlines]
        messages.add_message(request, messages.SUCCESS,
                             message=f'The {model._meta.verbose_name} #{form.instance.id} has been successfuly updated')
        return redirect(
            f"{reverse('core:change', kwargs={'app': app, 'model': model._meta.model_name})}?pk={form.instance.pk}")


class Delete(LoginRequiredMixin, View):
    def get(self, request, app, model):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, **request.GET.dict())
        form = AcceptForm()
        return render(request, f'{self.__class__.__name__.lower()}.html', locals())

    def post(self, request, app, model):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, **request.GET.dict())
        form = AcceptForm(request.POST or None, request.FILES or None)
        if not form.is_valid():
            return render(request, f'{self.__class__.__name__.lower()}.html', locals())
        data = form.cleaned_data
        if not data.get('accept', False):
            messages.add_message(request, level=messages.WARNING, message=f'Please check the `accept` field to delete '
                                                                          f'the {model._meta.verbose_name} #{obj.id}')
            return render(request, f'{self.__class__.__name__.lower()}.html', locals())
        obj.delete()
        return redirect(reverse('core:list', kwargs={'app': app, 'model': model._meta.model_name}))


class Action(LoginRequiredMixin, View):
    def post(self, request, app, model, action):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, **request.GET.dict())

        _action = getattr(model, 'conf', {}).get('change', {}).get('action', [])
        _action = [item for item in _action if item.get('title') == action]
        if len(_action) != 1: return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if eval(_action[0].get('condition')): eval(_action[0].get('statement'))
        return HttpResponseRedirect(request.GET.dict().get('redirect_to', None) or request.META.get('HTTP_REFERER'))


class Document(LoginRequiredMixin, View):
    def get(self, request, app, model, document):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, **request.GET.dict())
        return render(request, f'{self.__class__.__name__.lower()}/{document}.html', locals())


class Planning(LoginRequiredMixin, View):
    def get(self, request):
        events = Event().all()
        return render(request, f'{self.__class__.__name__.lower()}.html', locals())
