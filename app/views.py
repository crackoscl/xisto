from django.shortcuts import render
from django.views.generic import ListView,View
from .models import DancingDate

# Create your views here.


class Principal(View):
    
    def get(self,request):
        data = DancingDate.objects.all()
        return render(request,'app/index.html',context={'dancings':data})
    
    def post(self,request):
        pass