

from django.urls import path
from .views import Principal


urlpatterns = [
    path('',Principal.as_view(),name='principal'),
]
