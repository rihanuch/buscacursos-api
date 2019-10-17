from functools import reduce
from django.db import models
from django.utils import timezone
import pytz

uc_timezone = pytz.timezone('America/Santiago')


class Semestre(models.Model):
    year = models.IntegerField()
    semestre = models.IntegerField()

    objects = models.Manager()

    class Meta:
        unique_together = (
            'year',
            'semestre',
        )

    def __str__(self):
        return f'{self.year}-{self.semestre}'


class Campus(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.nombre


class Profesor(models.Model):
    nombre = models.CharField(max_length=200)

    objects = models.Manager()

    def agrupa_por_seccion(self, n_seccion):
        cupos_lista = []
        secciones = self.secciones.filter(seccion=n_seccion)
        for seccion in secciones:
            cupos_lista.extend(seccion.cupos.all())

        return cupos_lista

    @property
    def to_json(self):
        return [seccion.to_json for seccion in self.secciones.all()]

    def __str__(self):
        return self.nombre


class Ramo(models.Model):
    nombre = models.CharField(max_length=200)
    sigla = models.CharField(max_length=7)
    creditos = models.IntegerField()

    objects = models.Manager()

    class Meta:
        unique_together = (
            'nombre',
            'sigla',
            'creditos',
        )

    @property
    def to_json_agregado(self):

        horarios = [cupo['hora'] for cupo in Cupos.objects.values('hora').distinct()]
        horarios.sort()

        dataset = {'label': f'{self}', 'fill': '-1', 'data': [], 'hidden': True, 'spanGaps': False}
        for horario in horarios:
            if Cupos.objects.filter(seccion__ramo=self, hora=horario).count() == 0:
                disponibles = None
            else:
                disponibles = sum([cupo.disponibles for cupo in Cupos.objects.filter(seccion__ramo=self, hora=horario)])
            dataset['data'].append({'x': str(horario), 'y': disponibles})

        return dataset

    @property
    def to_json(self):

        horarios = [cupo['hora'] for cupo in Cupos.objects.values('hora').distinct()]
        horarios.sort()

        n_equivalentes = [seccion['seccion'] for seccion in self.secciones.values('seccion').distinct()]
        n_equivalentes.sort()

        cupos = []
        for seccion in self.secciones.all():
            for cupo in seccion.cupos.all():
                cupos.append(cupo)

        secciones = []
        for n_equivalente in n_equivalentes:
            dataset = {
                'label': f'{self.sigla}-{n_equivalente}',
                'fill': '-1',
                'data': []
            }
            cupos_seccion = self.agrupa_por_seccion(n_equivalente)
            for horario in horarios:
                cupos_horario = filter(lambda cupo: cupo.hora == horario, cupos_seccion)
                try:
                    disponibles = next(cupos_horario).disponibles
                except StopIteration:
                    disponibles = None
                dataset['data'].append({'x': str(horario), 'y': disponibles})

            secciones.append(dataset)

        return secciones

    def agrupa_por_seccion(self, n_seccion):
        cupos_lista = []
        secciones = self.secciones.filter(seccion=n_seccion)
        for seccion in secciones:
            cupos_lista.extend(seccion.cupos.all())

        return cupos_lista

    def __str__(self):
        return f'{self.sigla} - {self.nombre}'


class Seccion(models.Model):

    ramo = models.ForeignKey(Ramo,
                             related_name='secciones',
                             on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre,
                                 related_name='secciones',
                                 on_delete=models.CASCADE)
    profesores = models.ManyToManyField(Profesor, related_name='secciones')
    campus = models.ForeignKey(Campus,
                               related_name='secciones',
                               on_delete=models.CASCADE)
    seccion = models.IntegerField()
    nrc = models.IntegerField()
    retiro = models.BooleanField(default=True)
    ingles = models.BooleanField(default=False)

    objects = models.Manager()

    @property
    def to_json(self):
        dataset = {
            'label': str(self),
            'fill': False,
            'spanGaps': False,
            'data': [cupo.to_json for cupo in self.cupos.all().order_by('hora')]
        }
        return dataset

    class Meta:
        unique_together = ('ramo', 'seccion', 'semestre', 'nrc')

    def __str__(self):
        return f'{self.ramo.sigla}-{self.seccion} ({self.semestre})'


class Cupos(models.Model):

    seccion = models.ForeignKey(Seccion,
                                related_name='cupos',
                                on_delete=models.CASCADE)
    # registrar la hora a mano cuando se pase para
    # asi hacerlo con informacion agregadas
    hora = models.DateTimeField()
    disponibles = models.IntegerField()
    totales = models.IntegerField()

    objects = models.Manager()

    @property
    def to_json(self):
        return {'x': str(self.hora), 'y': self.disponibles}

    def __str__(self):
        return f'{self.seccion}: {self.disponibles}/{self.totales} ({self.hora})'
