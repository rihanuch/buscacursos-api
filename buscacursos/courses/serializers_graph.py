from .models import Ramo, Seccion, Profesor, Semestre, Campus, Cupos
from rest_framework import serializers


class GraphSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        if self.context['singular']:
            return obj.to_json
        else:
            return [obj.to_json_agregado]

    class Meta:
        model = Ramo
        fields = '__all__'


class GraphSerializerProfesor(serializers.ModelSerializer):
    def to_representation(self, obj):
        if self.context['singular']:
            return obj.to_json
        else:
            return [obj.to_json_agregado]

    class Meta:
        model = Profesor
        fields = '__all__'