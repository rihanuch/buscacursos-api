from .models import Ramo, Seccion, Profesor, Semestre, Campus, Cupos
from .serializers_generic import (RamoGenericSerializer,
                                  SeccionGenericSerializer,
                                  SemestreGenericSerializer,
                                  ProfesorGenericSerializer)
from rest_framework import serializers


def get_generic(instance: object, Model: object, Serializer: object, **kwargs):
    """Metodo generico para obtener informacion de segundo orden de relacion

    Reemplaza a get_<field_name> para evitar tener que reescribir lo mismo

    Params
    ------
    instance: self
        Debe recibir el self de la clase
    Model: models.Model
        Modelo de la base de datos
    Serializer: serializer.Serializer
        Serializador generico
    **kwargs
        Filtro que se quiere aplicar sobre el modelo

    Returns
    -------
    Serializer
        Serializador e informacion del modelo
    """
    queryset = Model.objects.filter(**kwargs).distinct()
    return Serializer(queryset, many=True, context=instance.context).data


class CuposSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cupos
        fields = ['hora', 'disponibles', 'totales', 'seccion']
        depth = 1


class RamoSerializer(serializers.HyperlinkedModelSerializer):

    cupos = serializers.SerializerMethodField('get_cupos')

    def get_cupos(self, ramo):
        return get_generic(self, Cupos, CuposSerializer, seccion__ramo=ramo)

    class Meta:
        model = Ramo
        fields = ['url', 'nombre', 'sigla', 'cupos']
        depth = 2


class SeccionSerializer(serializers.HyperlinkedModelSerializer):

    def to_representation(self, obj):
        return obj.to_json

    class Meta:
        model = Seccion
        fields = [
            'url', 'ramo', 'seccion', 'profesores', 'semestre', 'nrc',
            'retiro', 'ingles', 'campus', 'cupos'
        ]
        depth = 1


class SemestreSerializer(serializers.HyperlinkedModelSerializer):

    ramos = serializers.SerializerMethodField('get_ramos')

    def get_ramos(self, semestre):
        return get_generic(self,
                           Ramo,
                           RamoGenericSerializer,
                           secciones__semestre=semestre)

    class Meta:
        model = Semestre
        fields = ['url', 'year', 'semestre', 'ramos']


class CampusSerializer(serializers.HyperlinkedModelSerializer):

    ramos = serializers.SerializerMethodField('get_ramos')
    profesores = serializers.SerializerMethodField('get_profesores')

    def get_ramos(self, campus):
        return get_generic(self,
                           Ramo,
                           RamoGenericSerializer,
                           secciones__campus=campus)

    def get_profesores(self, campus):
        return get_generic(self,
                           Profesor,
                           ProfesorGenericSerializer,
                           secciones__campus=campus)

    class Meta:
        model = Campus
        fields = ['url', 'nombre', 'ramos', 'profesores']


class ProfesorSerializer(serializers.HyperlinkedModelSerializer):

    secciones = serializers.SerializerMethodField('get_secciones')
    semestres = serializers.SerializerMethodField('get_semestres')
    ramos = serializers.SerializerMethodField('get_ramo')

    def get_secciones(self, profesor):
        return get_generic(self,
                           Seccion,
                           SeccionGenericSerializer,
                           profesores=profesor)

    def get_semestres(self, profesor):
        return get_generic(self,
                           Semestre,
                           SemestreGenericSerializer,
                           secciones__profesores=profesor)

    def get_ramo(self, profesor):
        return get_generic(self,
                           Ramo,
                           RamoGenericSerializer,
                           secciones__profesores=profesor)

    class Meta:
        model = Profesor
        fields = ['url', 'nombre', 'secciones', 'semestres', 'ramos']
