from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse_lazy
from django.db import models
from django.apps import apps
from datetime import date


def upload_directory_file(instance, filename):
    return '{0}/{1}/{2}'.format(instance._meta.app_label, instance._meta.model_name, filename)


def choices(model, field):
    names = model.objects.all().values_list(field, flat=True)
    return [(None, '-')] + [(name, name) for name in names]


class Branch(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=100)
    created = models.DateTimeField(verbose_name="Cree le", auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Site"


class Grade(models.Model):
    code = models.CharField(verbose_name="Code", max_length=20)
    name = models.CharField(verbose_name="Nom", max_length=100)

    created = models.DateTimeField(verbose_name="Cree le", auto_now_add=True)

    def __str__(self):
        return f"{self.code}/{self.name}"

    class Meta:
        verbose_name = "Grade"


class Function(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=100)
    working_days = models.IntegerField(verbose_name="Jours de travail", default=0)

    created = models.DateTimeField(verbose_name="Cree le", auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Fonction"


class Direction(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=100)
    created = models.DateTimeField(verbose_name="Cree le", auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Direction"


class SubDirection(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=100)
    created = models.DateTimeField(verbose_name="Cree le", auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Sous-Direction"


class Service(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=100)
    created = models.DateTimeField(verbose_name="Cree le", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Service"


class Agreement(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=100)
    created = models.DateTimeField(verbose_name="Cree le", auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Agreement"


class Syndicat(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=100)
    created = models.DateTimeField(verbose_name="Cree le", auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Syndicat"


class PaymentMethod(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=100)
    created = models.DateTimeField(verbose_name="Cree le", auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Mode de paiement"


class Employee(models.Model):
    STATUS = (
        ('actif', 'Actif'),
        ('indisponibilite', 'Indisponibilite'),
        ('licenciement', 'Licenciement'),
        ('inactif', 'Inactif')
    )

    GENDERS = (("Male", "Homme"), ("Female", "Femme"))

    direction = models.ForeignKey(Direction, verbose_name="Direction", null=True, on_delete=models.SET_NULL)
    subDirection = models.ForeignKey(SubDirection, verbose_name="Sous-Direction/Technostructure", blank=True, null=True, on_delete=models.SET_NULL)
    service = models.ForeignKey(Service, verbose_name="Service", blank=True, null=True, on_delete=models.SET_NULL)

    function = models.ForeignKey(Function, verbose_name="Fonction", null=True, on_delete=models.SET_NULL)
    grade = models.ForeignKey(Grade, verbose_name="Grade", null=True, on_delete=models.SET_NULL)

    profile = models.ImageField(upload_to=upload_directory_file, blank=True, null=True, default=None)
    matricule = models.CharField("Matricule", unique=True, max_length=100, null=True, default=None)
    agreement = models.CharField("Type de contrat", max_length=10, choices=choices(Agreement, 'name'), null=True,
                                 default=None)

    first_name = models.CharField("Prenom", max_length=100, blank=True, null=True, default=None)
    middle_name = models.CharField("Post nom", max_length=100, blank=True, null=True, default=None)
    last_name = models.CharField("Nom", max_length=100, blank=True, null=True, default=None)

    n_cnss = models.CharField("N. CNSS", max_length=50, blank=True, null=True, default=None)
    n_inpp = models.CharField("N. INPP", max_length=50, blank=True, null=True, default=None)
    n_onem = models.CharField("N. ONEM", max_length=50, blank=True, null=True, default=None)

    gender = models.CharField("Genre", max_length=10, choices=GENDERS, null=True,
                              default="Male")
    marital_status = models.CharField("Etat civil", max_length=12,
                                      choices=(("Maried", "Marie"), ("Single", "Celibataire"), ("Widower", "Veuf(ve)")),
                                      default="Celibataire")
    spouse = models.CharField("Nom du cojoint(e)", max_length=100, blank=True, null=True, default=None)

    dob = models.DateField("Date de naissance", help_text='YYYY-MM-DD', blank=True, null=True, default=None)
    doj = models.DateField("Date d'entrée en fonction", help_text='YYYY-MM-DD', blank=True, null=True, default=None)

    mobile_number = PhoneNumberField("Numéro de mobile", null=True, default=None)
    address = models.TextField("Adresse permanente", blank=True, null=True, default=None)
    emergency_information = models.TextField("Information de contact d'urgence", null=True, default=None)

    syndicate = models.CharField("Syndicat", max_length=10, choices=choices(Syndicat, 'name'), blank=True, null=True,
                                 default=None)
    branch = models.CharField("Branch", max_length=10, choices=choices(Branch, 'name'))

    payment_method = models.CharField("Mode de paiement", max_length=10, choices=choices(PaymentMethod, 'name'))
    payer_name = models.CharField("Nom de la banque/Agent payeur", max_length=50, blank=True, null=True, default=None)
    pay_account = models.CharField("Numero de compte", max_length=50, blank=True, null=True, default=None)

    comment = models.TextField("Commentaire", blank=True, null=True, default=None)

    status = models.CharField(verbose_name="Status", max_length=20, choices=STATUS, default=STATUS[0][0])

    updated = models.DateTimeField(verbose_name="Mise à jour le", auto_now=True)
    created = models.DateTimeField(verbose_name="Créée le", auto_now_add=True)

    conf = {
        'icon': 'users',
        'description': 'The list of all employee of the company',
        'entry': reverse_lazy('core:list', kwargs={'app': 'employee', 'model': 'employee'}),
        'list': {
            'display': [('matricule', 'Matricule'), ('direction', 'Direction'), ('function', 'Fonction'), ('last_name', 'Nom'), ('first_name', 'Prenom'), ('status', 'Status'), ('updated', 'Mis à jour le')],
            'filter': ['direction', 'subDirection', 'function', 'grade', 'gender', 'marital_status', 'branch', 'payment_method', 'status', 'doj'],
            'action': [{
                'method': 'GET',
                'href': reverse_lazy('core:create', kwargs={'app': 'employee', 'model': 'employee'}),
                'class': 'btn btn-primary',
                'title': 'Ajouter'
            }]
        },
        'change': {
            'form': {
                'fields': ['direction', 'subDirection', 'service', 'function',
                           'grade', 'matricule', 'agreement', 'branch',
                           'profile', 'last_name', 'middle_name', 'first_name', 'dob',
                           'gender', 'marital_status', 'spouse', 'mobile_number', 'address',
                           'doj', 'n_cnss', 'n_inpp', 'n_onem',
                           'payment_method', 'pay_account', 'payer_name', 'emergency_information', 'comment', 'status'],
                'inlines': [{
                    'app': 'core',
                    'model': 'user',
                    'fields': ['email', 'groups']
                }, {
                    'app': 'employee',
                    'model': 'child',
                    'fields': ['full_name', 'dob', 'birth_certificate']
                }, {
                    'app': 'employee',
                    'model': 'document',
                    'fields': ['name', 'doc']
                }]
            },
            'action': [{
                'method': 'GET',
                'href': reverse_lazy('core:delete', kwargs={'app': 'employee', 'model': 'employee'}),
                'class': 'btn btn-danger',
                'title': 'Delete',
                'condition': 'True'
            }, {
                'method': 'GET',
                'href': reverse_lazy('core:document', kwargs={'app': 'employee', 'model': 'employee', 'document': 'employee'}),
                'class': 'btn btn-info',
                'title': 'Document',
                'condition': 'True'
            }]
        },
        'create': {
            'form': {
                'fields': ['direction', 'subDirection', 'service', 'function',
                           'grade', 'matricule', 'agreement', 'branch',
                           'profile', 'last_name', 'middle_name', 'first_name', 'dob',
                           'gender', 'marital_status', 'spouse', 'mobile_number', 'address',
                           'doj', 'n_cnss', 'n_inpp', 'n_onem',
                           'payment_method', 'pay_account', 'payer_name', 'emergency_information', 'comment', 'status'],
                'inlines': []
            }
        },
        'read': {
            'action': [{
                'method': 'GET',
                'href': reverse_lazy('core:document',
                                     kwargs={'app': 'employee', 'model': 'employee', 'document': 'employee'}),
                'class': 'btn btn-info',
                'title': 'Document',
                'condition': 'True'
            }]
        }
    }

    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def children(self):
        return Child.objects.select_related().filter(employee=self)

    def documents(self):
        return Document.objects.select_related().filter(employee=self)

    def approvers(self):
        model = apps.get_model('core', model_name='approver')
        return model.objects.filter(model='employee.Employee')

    def approvals(self):
        model = apps.get_model('core', model_name='approval')
        return model.objects.filter(model='employee.Employee', _pk=self.pk)

    def __str__(self):
        return f"{self.matricule}/{self.full_name()}"


class Child(models.Model):
    employee = models.ForeignKey(Employee, verbose_name="Employee", null=True, on_delete=models.SET_NULL)
    full_name = models.CharField(verbose_name="Nom complet", max_length=100)

    dob = models.DateField(verbose_name="Date de naissance", help_text="YYYY-MM-DD")
    birth_certificate = models.FileField(verbose_name="Attestation de naissance", upload_to=upload_directory_file)

    updated = models.DateTimeField(verbose_name="Mise à jour le", auto_now=True)
    created = models.DateTimeField(verbose_name="Créée le", auto_now_add=True)

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        verbose_name = "Enfant"


class Document(models.Model):
    employee = models.ForeignKey(Employee, verbose_name="Employee", null=True, on_delete=models.SET_NULL)

    name = models.CharField(verbose_name="Nom", max_length=100)
    doc = models.FileField(verbose_name="Document", upload_to=upload_directory_file)

    updated = models.DateTimeField(verbose_name="Mise à jour le", auto_now=True)
    created = models.DateTimeField(verbose_name="Créée le", auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Document"
