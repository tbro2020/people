from django.urls import path
from core.views import *

app_name = 'core'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('list/<str:app>/<str:model>', List.as_view(), name='list'),
    path('read/<str:app>/<str:model>', List.as_view(), name='read'),
    path('create/<str:app>/<str:model>', Create.as_view(), name='create'),
    path('change/<str:app>/<str:model>', Change.as_view(), name='change'),
    path('delete/<str:app>/<str:model>', Delete.as_view(), name='delete'),
    path('action/<str:app>/<str:model>', List.as_view(), name='action'),

    path('document/<str:app>/<str:model>/<str:document>', Document.as_view(), name='document'),

    path('import/<str:app>/<str:model>', List.as_view(), name='import'),
    path('export/<str:app>/<str:model>', List.as_view(), name='export'),
]