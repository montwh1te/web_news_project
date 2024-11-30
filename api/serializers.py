from rest_framework import serializers
from .models import Time, Jogador, Presidente, Tecnico, Estadio

class PresidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presidente
        fields = ['nome', 'foto']

class TecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnico
        fields = ['nome', 'foto']

class EstadioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estadio
        fields = ['nome', 'foto']

class JogadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jogador
        fields = ['nome', 'posicao', 'foto']

class TimeSerializer(serializers.ModelSerializer):
    presidente = PresidenteSerializer()
    tecnico = TecnicoSerializer()
    estadio = EstadioSerializer()
    jogadores = JogadorSerializer(many=True, source='jogador_set')

    class Meta:
        model = Time
        fields = ['nome', 'ano_fundacao', 'presidente', 'tecnico', 'estadio', 'jogadores']