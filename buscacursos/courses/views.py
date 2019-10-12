from .models import Ramo, Seccion, Profesor, Semestre, Campus, Cupos
from rest_framework import viewsets
from buscacursos.courses.serializers import (RamoSerializer, SeccionSerializer,
                                             ProfesorSerializer,
                                             SemestreSerializer,
                                             CampusSerializer, CuposSerializer)
from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import action
from rest_framework.response import Response
import json


class CuposViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cupos to be viewed or edited.
    """
    queryset = Cupos.objects.all()
    serializer_class = CuposSerializer


class CampusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows campus to be viewed or edited.
    """
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer


class SemestreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows semestre to be viewed or edited.
    """
    queryset = Semestre.objects.all()
    serializer_class = SemestreSerializer


class ProfesorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profesores to be viewed or edited.
    """
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer


class RamoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ramos to be viewed or edited.
    """
    queryset = Ramo.objects.all()
    serializer_class = RamoSerializer

    @action(methods=['GET'],
            detail=True,
            url_path='semestre/(?P<semestre_pk>[^/.]+)')
    def by_semester(self, request, semestre_pk, pk=None):
        ramo = self.get_object()
        semestre = Semestre.objects.get(pk=semestre_pk)
        secciones = ramo.secciones.filter(semestre=semestre)
        respuesta = [
            SeccionSerializer(seccion, context={
                'request': request
            }).data for seccion in secciones
        ]
        return Response(respuesta)


class SeccionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows secciones to be viewed or edited.
    """
    queryset = Seccion.objects.all()
    serializer_class = SeccionSerializer


def graficar_ramos(request, dpto):
    ramos = Ramo.objects.filter(sigla__contains=dpto.upper()).order_by('sigla')
    datasets = [ramo.to_json_agregado for ramo in ramos]
    datasets[0]['fill'] = 'origin'
    datasets = json.dumps(datasets)
    template = loader.get_template('courses/ramo.html')

    ejes = {
        'titulo': f'Disponibilidad de ramos de {dpto.upper()}',
        'scheme': 'tableau.HueCircle19',
        }
    ejes = json.dumps(ejes)
    return HttpResponse(
        template.render({
            'datasets': datasets,
            'ejes': ejes,
        }, request))


def graficar_por_ramo(request, sigla):
    ramo = Ramo.objects.get(sigla__iexact=sigla.lower())

    datasets = ramo.to_json
    datasets[0]['fill'] = 'origin'
    datasets = json.dumps(datasets)
    template = loader.get_template('courses/ramo.html')

    ejes = {
        'titulo': f'Disponibilidad de ramo {ramo.sigla.upper()}: {ramo.nombre}',
        'scheme': 'office.Metro6'
        }
    ejes = json.dumps(ejes)
    return HttpResponse(
        template.render({
            'datasets': datasets,
            'ejes': ejes,
        }, request))
