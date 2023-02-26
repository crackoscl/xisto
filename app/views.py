from django.shortcuts import render
from django.views.generic import ListView,View,TemplateView
from django.http import JsonResponse
from .models import DancingDate


class Principal(TemplateView):
    template_name = 'app/index.html'

class AppPage(View):
    
    def get(self,request):
        return JsonResponse({'data': list(DancingDate.objects.all().values()) })
        
    def post(self,request):
        if request.POST:
            DancingDate.objects.create(
                sname = request.POST.get('sname'),
                ddate = request.POST.get('ddate'),
                ntime = request.POST.get('ntime'),
                scontact = request.POST.get('scontact')
            )
            return JsonResponse({'message':'Guardado'})
        else:
            return JsonResponse({'message':'Error'})



        