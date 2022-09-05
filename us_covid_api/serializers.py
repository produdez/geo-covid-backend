from .models import State, Report
from rest_framework import serializers

class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name', 'initials']

class ReportSerializer(serializers.HyperlinkedModelSerializer):
    state = StateSerializer()
    class Meta:
        model = Report
        fields = [
            'date', 'state', 
            'death', 'death_confirmed',
            'hospitalized',
            'positive', 'negative',
            'recovered'
        ]
