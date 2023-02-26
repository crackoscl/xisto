from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework import permissions
from .models import DancingDate
from .serializer import DancingSerializer


class Principal(TemplateView):
    template_name = 'index.html'


class DacingView(viewsets.ModelViewSet):
    queryset = DancingDate.objects.all()
    serializer_class = DancingSerializer
    permission_classes  = [permissions.AllowAny]

