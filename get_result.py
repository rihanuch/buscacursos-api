import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "buscacursos.settings")
django.setup()

from urllib.request import urlopen
from pprint import pprint
from bs4 import BeautifulSoup
from collections import namedtuple
from buscacursos.courses.models import Semestre, Campus, Profesor, Ramo, Seccion, Cupos
from datetime import datetime
import pytz



local_timezone = pytz.timezone('Chile/Continental')

Ramox = namedtuple('Ramox', [
    'nrc', 'sigla', 'retiro', 'ingles', 'seccion', 'nombre', 'profesor',
    'campus', 'cred', 'total', 'disponible'
])

BUSACURSOS = 'http://buscacursos.uc.cl/?'

SIGLA = 'cxml_sigla='
SEM = 'cxml_semestre='
BASIC_URL = 'http://buscacursos.uc.cl/?'


def generate_search(sigla, semester, year):
    url = f'{BASIC_URL}{SEM}{year}-{semester}&{SIGLA}{sigla}#resultados'
    return BeautifulSoup(urlopen(url).read(), 'lxml')


def get_tags(sigla, semester, year):
    result = generate_search(sigla, semester, year)
    return result.findAll(
        "tr", {"class": ["resultadosRowPar", "resultadosRowImpar"]})


# result = BeautifulSoup(urlopen('http://buscacursos.uc.cl/?cxml_semestre=2019-2&cxml_sigla=iic1#resultados').read(), 'lxml')

# tags = result.findAll("tr", {"class": ["resultadosRowPar", "resultadosRowImpar"]})

siglas = [
    'imm', 'iiq', 'iic', 'iee', 'ict', 'ics', 'icm', 'ich', 'ice', 'icc',
    'idi', 'ing'
]

campuses = set()
profesores = set()
ramos = []
semm = []

# for sigg in siglas:
#     print(sigg)
#     for year in range(2018, 2020):
#         for semestre in range(1, 3):

#             semestre_model = Semestre.objects.get(year=year, semestre=semestre)

#             # nivel del ramo (1000, 2000, 3000)
#             for nivel in range(1, 4):

#                 tags = get_tags(f'{sigg}{nivel}', semestre, year)

#                 for seccion in range(len(tags)):    

#                     nrc = int(tags[seccion].select('td')[0].getText())
#                     sigla = tags[seccion].select_one(
#                         '.tooltipInfoCurso').getText()[1:]
#                     retiro = (
#                         tags[seccion].select('td')[2].getText()[1:-1] == 'SI')
#                     ingles = (tags[seccion].select('td')[3].getText() == 'SI')
#                     n_seccion = int(tags[seccion].select('td')[4].getText())
#                     nombre = tags[seccion].select('td')[7].getText()
#                     profesor = tags[seccion].select('td')[8].getText()
#                     campus = tags[seccion].select('td')[9].getText()
#                     creds = int(tags[seccion].select('td')[10].getText())

#                     profesor = profesor.split(', ')
#                     # for prof in profesor:
#                     #     profesores.add(prof)
#                     profesores_models = []
#                     for prof in profesor:
#                         prof_model = Profesor.objects.get(nombre=prof)
#                         profesores_models.append(prof_model)
                    

#                     ramo_model = Ramo.objects.get(sigla=sigla, nombre=nombre, creditos=creds)

#                     try:
#                         campus_model = Campus.objects.get(nombre=campus)
#                     except:
#                         campus_model = Campus(nombre=campus)
#                         campus_model.save()

#                     # seccion:
#                     # ramo
#                     # semestre
#                     # profesores
#                     # campus
#                     # seccion
#                     # nrc
#                     # retiro
#                     # ingles

#                     seccion_model = Seccion(ramo=ramo_model, semestre=semestre_model, campus=campus_model, seccion=n_seccion, nrc=nrc, retiro=retiro, ingles=ingles)
#                     seccion_model.save()

#                     for prof in profesores_models:
#                         seccion_model.profesores.add(prof)

#                     seccion_model.save()

#                     rows = tags[seccion].select('td')[11:13]

#                     if semestre == 1:
#                         mes = 3
#                     if semestre == 2:
#                         mes = 7


#                     hora = datetime(year=year, month=mes, day=1, hour=8, minute=0, second=0, tzinfo=local_timezone)
#                     cupos_totales = int(rows[0].getText())
#                     cupos_disponibles = int(rows[1].getText())

#                     cupos_model = Cupos(hora=hora, disponibles=cupos_disponibles, totales=cupos_totales, seccion=seccion_model)
#                     cupos_model.save()

#                     # ramos.append((sigla, nombre, creds))
#                     # campuses.add(campus)

#                     secc = Ramox(nrc, sigla, retiro, ingles, n_seccion, nombre,
#                                  profesor, campus, creds, cupos_totales,
#                                  cupos_disponibles)
#                     # secciones.append(secc)
#             # se = (year, semestre)
#             # semm.append(se)

# for prof in profesores:
#     p = Profesor(nombre=prof)
#     p.save()

# for ramo in set(ramos):
#     ram = Ramo(sigla=ramo[0], nombre=ramo[1], creditos=ramo[2])
#     ram.save()

# for camp in campuses:
#     ca = Campus(nombre=camp)
#     ca.save()

# for sem in set(semm):
#     se = Semestre(year=sem[0], semestre=sem[1])
#     se.save()