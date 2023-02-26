

from django.urls import path
from .views import Principal,AppPage

app_name = 'app'

urlpatterns = [
    path('',Principal.as_view(),name='principal'),
    path('app/',AppPage.as_view(),name='AppPage')
]
