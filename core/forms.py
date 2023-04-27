from crispy_forms.layout import Layout, Row, Column
from crispy_forms.helper import FormHelper
from django import forms

from django.apps import apps


class AcceptForm(forms.Form):
    accept = forms.BooleanField(help_text='Cochez pour continuer l\'action')


class Row3Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        for field in self.fields:
            if not isinstance(self.fields[field].widget, forms.widgets.Textarea): continue
            self.fields[field].widget.attrs['rows'] = '2'

        if self._meta.model._meta.model_name in ['user', 'child', 'document']: return

        fields = [Column(key, css_class=f'col-4 mb-0') for key, value in self.fields.items()]
        fields = [fields[x:x + 3] for x in range(0, len(fields), 3)]
        fields = [Row(*field, css_class='form-row') for field in fields]
        self.helper.layout = Layout(*fields)


class InlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
