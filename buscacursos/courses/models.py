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

        horarios = set()

        for cupo in Cupos.objects.all():
            horarios.add(cupo.hora)

        horarios = sorted(horarios)

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

        horarios = set()

        for cupo in Cupos.objects.all():
            horarios.add(cupo.hora)

        equivalentes = set(
            [seccion.seccion for seccion in self.secciones.all()])

        cupos = []

        for seccion in self.secciones.all():
            for cupo in seccion.cupos.all():
                cupos.append(cupo)

        secciones = []
        for num, n_seccion in enumerate(equivalentes):
            if num == 0:
                color = 'origin'
            else:
                color = '-1'
            dataset = {
                'label': f'{self.sigla}-{n_seccion}',
                'fill': color,
                'data': [],
            }
            for cupo in cupos:
                if cupo.seccion.seccion == n_seccion:
                    dataset['data'].append(cupo.to_json)

            secciones.append(dataset)

        return secciones

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
            'data': [cupo.to_json for cupo in self.cupos.all()]
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
