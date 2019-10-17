"""buscacursos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from buscacursos.courses import views

router = routers.DefaultRouter()
router.register(r'ramos', views.RamoViewSet)
router.register(r'secciones', views.SeccionViewSet)
router.register(r'profesores', views.ProfesorViewSet)
router.register(r'semestres', views.SemestreViewSet)
router.register(r'campus', views.CampusViewSet)
router.register(r'cupos', views.CuposViewSet)
router.register(r'graph/ramo(?P<singular>s?)/(?P<sigla>[a-zA-Z0-9_]{1,7})', views.GraphSet, base_name='ramo_especifico')
router.register(r'graph/profesor(?P<singular>s?)/(?P<identificador>\d+)', views.GraphSet, base_name='profesor_especifico')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('search/', views.SearchList.as_view(), name='search_list'),
    path('graph/ramo/<str:sigla>', views.graficar_por_ramo, name='ramo_especifico'),
    path('graph/ramos/<str:dpto>', views.graficar_ramos, name='ramos_total'),
    path('graph/profesor/<int:identificador>', views.graficar_profesor, name='profesor_especifico'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
