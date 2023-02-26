
from rest_framework import serializers
from .models import DancingDate



class DancingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DancingDate
        fields = '__all__'

    
