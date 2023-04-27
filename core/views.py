from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.apps import apps

from django.forms import modelform_factory, inlineformset_factory
from core.forms import AcceptForm, Row3Form, InlineForm
from core.filters import filterset_factory


class Home(LoginRequiredMixin, View):
    def get(self, request):
        cards = {model._meta.verbose_name_plural: model.objects.all().count() for model in apps.get_models()}
        return render(request, f'{self.__class__.__name__.lower()}.html', locals())


class Read(LoginRequiredMixin, View):
    def get(self, request, app, model, pk):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, pk=pk)

        inlines = []
        form = modelform_factory(model)(instance=obj)

        for inline in getattr(model, 'conf', {}).get('change', {}).get('form', {}).get('inlines', []):
            _model = apps.get_model(inline.get('app'), model_name=inline.get('model'))
            _form = inlineformset_factory(model, _model, extra=1)(instance=obj)
            inlines.append(_form)
        return render(request, f'{self.__class__.__name__.lower()}.html', locals())


class List(LoginRequiredMixin, View):
    def get(self, request, app, model):
        model = apps.get_model(app, model_name=model)

        fields = {'filter': getattr(model, 'conf', {}).get('list', {}).get('filter', [])}
        _filter = filterset_factory(model, **fields)(request.GET, queryset=model.objects.select_related().all())
        filter_form = _filter.form
        qs = _filter.qs
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
            return render(request, f'{self.__class__.__name__}.html', locals())

        form.save()
        [inline.save() for inline in inlines]
        messages.add_message(request, messages.SUCCESS,
                             message=f'The {model._meta.verbose_name} has been successfuly created')
        return redirect(
            f"{reverse('core:change', kwargs={'app': app, 'model': model._meta.model_name})}?pk={form.instance.pk}")


class Change(LoginRequiredMixin, View):
    def get(self, request, app, model):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, **request.GET.dict())

        inlines = []
        fields = getattr(model, 'conf', {}).get('change', {}).get('form', {}).get('fields', '__all__')
        form = modelform_factory(model, fields=fields, form=Row3Form)(instance=obj)

        for inline in getattr(model, 'conf', {}).get('change', {}).get('form', {}).get('inlines', []):
            _fields = inline.get('fields', '__all__')
            _model = apps.get_model(inline.get('app'), model_name=inline.get('model'))
            _form = inlineformset_factory(model, _model, form=Row3Form, fields=_fields, exclude=(model._meta.model_name,), extra=1, can_delete=True)(instance=obj)
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
            return render(request, f'{self.__class__.__name__}.html', locals())

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
        return render(request, f'{self.__class__.__name__}.html', locals())

    def post(self, request, app, model):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, **request.GET.dict())
        form = AcceptForm(request.POST or None, request.FILES or None)
        if not form.is_valid():
            return render(request, f'{self.__class__.__name__}.html', locals())
        data = form.cleaned_data
        if not data.get('accept', False):
            messages.add_message(request, level=messages.WARNING, message=f'Please check the `accept` field to delete '
                                                                          f'the {model._meta.verbose_name} #{obj.id}')
            return render(request, f'{self.__class__.__name__}.html', locals())
        obj.delete()
        return redirect(reverse('core:list', kwargs={'app': app, 'model': model._meta.model_name}))


class Action(LoginRequiredMixin, View):
    def post(self, request, app, model, pk, action):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, pk=pk)

        action = getattr(model, 'conf', {}).get('change', {}).get('action', {}).get(action, {})
        if eval(action.get('condition', 'False')):
            return redirect('')
        eval(action.get('statement', 'False'))
        messages.add_message(request, level=messages.SUCCESS,
                             message=f'Successful action on {model._meta.verbose_name}')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class Document(LoginRequiredMixin, View):
    def get(self, request, app, model, document):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, **request.GET.dict())
        return render(request, f'{self.__class__.__name__.lower()}/{document}.html', locals())