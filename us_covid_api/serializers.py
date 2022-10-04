from ast import Global
from .models import GlobalReport, GlobalReport, Polygon, State, Report
from rest_framework import serializers

class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name', 'initials']

class PolygonSerializer(serializers.HyperlinkedModelSerializer):
    # BUG: serializer return some null state when using nested State object inside Polygon so i just hack it here :)
    # Resolve by just adding needed files of State on to Polygon itself (in models.py)
    class Meta:
        model = Polygon
        fields = ['state_id', 'type', 'state_name', 'state_initials','coordinates',]

class ReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Report
        fields = [
            'date', 'state_id',
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

class GlobalReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GlobalReport
        fields = [
            'date', 'states',
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
