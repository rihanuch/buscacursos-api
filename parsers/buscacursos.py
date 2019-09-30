from urllib.request import urlopen
from pprint import pprint
from bs4 import BeautifulSoup
import json

BUSACURSOS = 'http://buscacursos.uc.cl/?'

SIGLA = 'cxml_sigla='
SEM = 'cxml_semestre='


def cupos_ramo(sigla_ramo, semestre):
    busqueda = f'{BUSACURSOS}&{SEM}{semestre}&{SIGLA}{sigla_ramo}#resultados'
    result = BeautifulSoup(urlopen(busqueda).read(), 'html5lib')

    existe = result.findAll(text='La búsqueda no produjo resultados.')
    if len(existe) > 1:
        return []

    tags = result.findAll(
        "tr", {"class": ["resultadosRowPar", "resultadosRowImpar"]})
    secciones = []
    # 4 es seccion
    totales = 0
    disponibles = 0
    year, semester = semestre.split('-')
    year, semester = int(year), int(semester)
    for seccion in range(len(tags)):
        n_seccion = int(tags[seccion].select('td')[4].getText())

        profesor = tags[seccion].select('td')[8].getText()
        profesores = profesor.split(', ')
        profesores = [prof.replace(' ', '_').lower() for prof in profesores]
        nombre = tags[seccion].select('td')[7].getText()

        rows = tags[seccion].select('td')[11:13]
        cupos_totales = int(rows[0].getText())
        cupos_disponibles = int(rows[1].getText())

        totales += cupos_totales
        disponibles += cupos_disponibles

        secciones.append({
            'semester': semester,
            'year': year,
            'total': cupos_totales,
            'available': cupos_disponibles,
            'section': n_seccion,
            'teachers': profesores, 
            'name': nombre})

    return secciones


def ramo_existe(sigla_ramo, semestre):
    busqueda = f'{BUSACURSOS}&{SEM}{semestre}&{SIGLA}{sigla_ramo}#resultados'
    result = BeautifulSoup(urlopen(busqueda).read(), 'html5lib')

    res = result.findAll('div', {'style': 'min-width:88px;margin-left:5px'})
    ramos = list(set([ramo.getText()[1:] for ramo in res]))
    return ramos

# ramos = ['ics2523', 'iic2154', 'ics3313', 'iic3113', 'ics3413',
#          'iic3745', 'iic2343', 'iic2333', 'iic3143', 'ics3013', ]


def buscar_ramo(sigla):

    ramos = [f'{sigla}{i}' for i in range(1, 4)]

    existentes = []

    for ramo in ramos:
        # historico = {}
        for year in range(2018, 2020):
            # historico[year] = {}
            existe_semestres = []
            for sem in range(1, 3):
                existentes.extend(ramo_existe(ramo, f'{year}-{sem}'))

    return list(set(existentes))


siglas = ['imm', 'iiq', 'iic', 'iee', 'ict', 'ics',
          'icm', 'ich', 'ice', 'icc', 'idi', 'ing']


with open('data/existen.json', 'r', encoding='utf8') as file:
    data = json.load(file)
    export = []
    for key, value in data.items():
        print(key)
        # export[key] = {}
        for ramo in value:
            print(ramo)
            ramo_dict = {
                'name': '',
                'id': ramo.lower(),
                'given': []
            }
            for year in range(2018, 2020):
                for semestre in range(1, 3):
                    sections = cupos_ramo(ramo, f'{year}-{semestre}')
                    if sections == []:
                        continue
                    else:
                        ramo_dict['name'] = sections[0]['name']
                        for section in sections:
                            del section['name']
                    ramo_dict['given'].extend(sections)
            # print(ramo_dict)
            export.append(ramo_dict)

    with open('data/cupos.json', 'w', encoding='utf8') as out:
        json.dump(export, out)
