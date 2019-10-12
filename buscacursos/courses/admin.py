from django.contrib import admin
from .models import Semestre, Campus, Profesor, Ramo, Seccion, Cupos
# Register your models here.

admin.site.register(Semestre)
admin.site.register(Campus)
admin.site.register(Profesor)
admin.site.register(Ramo)
admin.site.register(Seccion)
admin.site.register(Cupos)