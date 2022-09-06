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
            'death', 'death_confirmed', 'death_increase', 'death_probable',
            'positive', 'positive_increase', 'positive_cases_viral',
            'negative', 'negative_increase',
            'hospitalized_cumulative', 'hospitalized_increase', 'hospitalized_currently',
            'in_icu_cumulative', 'in_icu_currently',
            'on_ventilator_cumulative', 'on_ventilator_currently',
            'recovered',
            'total_tests_people_viral', 'total_tests_people_viral_increase',
            'total_tests_viral', 'total_tests_viral_increase',
            'positive_tests_viral', 'negative_tests_viral'
        ]
