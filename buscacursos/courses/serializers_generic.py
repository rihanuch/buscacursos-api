from .models import Ramo, Seccion, Profesor, Semestre, Campus
from rest_framework import serializers


class RamoGenericSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ramo
        fields = ['url', 'nombre', 'sigla']


class SeccionGenericSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Seccion
        fields = ['url', 'semestre']
        depth = 1


class SemestreGenericSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Semestre
        fields = ['url', 'year', 'semestre']


class ProfesorGenericSerializer(serializers.HyperlinkedModelSerializer):
    class Meta(object):
        model = Profesor
        fields = ['url', 'nombre']
