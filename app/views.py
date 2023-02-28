from django.shortcuts import render
from django.views.generic import TemplateView
#from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView,CreateAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import DancingDate
from .serializer import DancingSerializer


class Principal(TemplateView):
    template_name = 'index.html'


class DancingListApiView(ListAPIView):
    serializer_class = DancingSerializer
    queryset = DancingDate.objects.all()


class DacingCreateApiView(CreateAPIView):
    serializer_class = DancingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Dacing creado correctamente'},status= status.HTTP_201_CREATED)
        return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)


class DacingRetriApiView(RetrieveAPIView):
    serializer_class = DancingSerializer
    #queryset = DancingDate.objects.all()

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.all()


class DacingDestroyApiview(DestroyAPIView):
    serializer_class = DancingSerializer
    
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.all()
    
    def delete(self,request,pk=None):
        dacing = self.get_queryset().filter(id=pk).first()
        if dacing:
            dacing.delete()
            return Response({'message':'Dacing Eliminado correctamente'},status= status.HTTP_200_OK)
        return Response({'error':'Dacing no encontrado'},status= status.HTTP_400_BAD_REQUEST)


class DacingUpdateApiview(UpdateAPIView):
    serializer_class = DancingSerializer
    
    
    def get_queryset(self,pk):
        return self.get_serializer().Meta.model.objects.filter(pk=pk).first()

    def patch(self, request,pk=None):
        if self.get_queryset(pk):
            dancing_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(dancing_serializer.data,status=status.HTTP_200_OK)
        return Response({'error':'no existe un dacing con estos datos'},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk=None):
        if self.get_queryset(pk):
            dancing_serializer = self.serializer_class(self.get_queryset(pk),data=request.data)
            if dancing_serializer.is_valid():
                dancing_serializer.save()
                return Response(dancing_serializer.data,status=status.HTTP_200_OK)
            return Response(dancing_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
