from .models import State, Report
from rest_framework import serializers

# TODO: update later
class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        fields = ['name', 'initials']


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Report
        fields = ['date', 'state', 'death', 'positive', 'negative']
