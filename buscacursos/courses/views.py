from .models import Ramo, Seccion, Profesor, Semestre, Campus, Cupos
from rest_framework import viewsets
from buscacursos.courses.serializers import (RamoSerializer, SeccionSerializer,
                                             ProfesorSerializer,
                                             SemestreSerializer,
                                             CampusSerializer, CuposSerializer)
from buscacursos.courses.serializers_graph import (GraphSerializer, GraphSerializerProfesor)
from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import action
from rest_framework.response import Response
import json
from django.db.models import Q
from django.views import generic
from django.urls import reverse
from itertools import chain


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


class GraphSet(viewsets.ModelViewSet):

    def get_serializer_context(self):
        singular = (self.kwargs['singular'].lower() != 's')
        return {'singular': singular}

    def get_serializer_class(self, *args, **kwargs):
        if 'sigla' in self.kwargs.keys():
            return GraphSerializer
        else:
            return GraphSerializerProfesor

    def get_queryset(self):
        singular = (self.kwargs['singular'].lower() != 's')
        if 'sigla' in self.kwargs.keys():
            sigla = self.kwargs['sigla'].lower()
            if singular:
                return Ramo.objects.filter(sigla__iexact=sigla)
            else:
                return Ramo.objects.filter(sigla__contains=sigla.upper()).order_by('sigla')
        if 'identificador' in self.kwargs.keys():
            identificador = self.kwargs['identificador']
            return Profesor.objects.filter(pk=identificador)


def graficar_profesor(request, identificador):
    template = loader.get_template('courses/ramo.html')
    profesor = Profesor.objects.get(pk=identificador)
    info = {
        'titulo': f'Disponibilidad de ramos de {profesor}',
        'scheme': 'tableau.HueCircle19',
        'url': request.path,
        }
    print(request.path)
    info = json.dumps(info)
    return HttpResponse(
        template.render({
            'info': info,
            'titulo': f'Disponibilidad de ramos de {profesor}',
        }, request))


def graficar_ramos(request, dpto):
    template = loader.get_template('courses/ramo.html')

    info = {
        'titulo': f'Disponibilidad de ramos de {dpto.upper()}',
        'scheme': 'tableau.HueCircle19',
        'url': request.path,
        }
    info = json.dumps(info)
    return HttpResponse(
        template.render({
            'info': info,
            'titulo': f'Disponibilidad de ramos de {dpto.upper()}',
        }, request))


def graficar_por_ramo(request, sigla):

    ramo = Ramo.objects.get(sigla__iexact=sigla.upper())

    template = loader.get_template('courses/ramo.html')

    info = {
        'titulo': f'Disponibilidad de ramo {ramo.sigla.upper()}: {ramo.nombre}',
        'scheme': 'office.Metro6',
        'url': request.path,
        }
    info = json.dumps(info)
    return HttpResponse(
        template.render({
            'info': info,
            'titulo': f'Disponibilidad de ramo {ramo.sigla.upper()}: {ramo.nombre}',
        }, request))


class SearchList(generic.ListView):

    template_name = 'courses/search.html'
    context_object_name = 'ramos'
    paginate_by = 50

    def get_queryset(self):
        parameter = self.request.GET.get('search')
        search_ramos = (Q(sigla__icontains=parameter) | Q(nombre__icontains=parameter))
        profesores = Profesor.objects.filter(nombre__icontains=parameter).order_by('nombre')
        ramos = Ramo.objects.filter(search_ramos).distinct().order_by('sigla')
        resultado = list(chain(profesores, ramos))
        return resultado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('search')
        context['titulo'] = f'Resultados de búsqueda \'{context["query"]}\''
        context['multiple'] = False
        context['profesores'] = False
        if len(context['object_list']) > 0:
            if isinstance(context['object_list'][0], Profesor):
                context['profesores'] = True
            context['multiple'] = True
            context['multiple_url'] = reverse('ramos_total', kwargs={'dpto': context['query']})
        return context