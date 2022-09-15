from django.http import HttpResponse
from .models import State, Report
from rest_framework import viewsets, generics
from us_covid_api.serializers import StateSerializer, ReportSerializer
from rest_framework.exceptions import NotFound
from datetime import datetime, time, timedelta
from django.utils.timezone import make_aware
from rest_framework.renderers import JSONRenderer


class StatesDetail(generics.ListAPIView):
    '''
        Detail of all states
    '''
    queryset = State.objects.all()
    serializer_class = StateSerializer
class StateDetail(generics.RetrieveAPIView):
    '''
        Detail of a state
        lookup by id
    '''
    lookup_field = 'id'
    queryset = State.objects.all()
    serializer_class = StateSerializer

class StateByInitials(generics.RetrieveAPIView):
    '''
        Detail of a state
        lookup by initials
    '''
    lookup_field = 'initials'
    queryset = State.objects.all()
    serializer_class = StateSerializer
class StateByName(generics.RetrieveAPIView):
    '''
        Detail of a state
        lookup by name
    '''
    lookup_field = 'name'
    queryset = State.objects.all()
    serializer_class = StateSerializer

class Reports(generics.ListAPIView):
    '''
        All reports
    '''
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class StateReports(generics.ListAPIView):
    '''
        All report (all days) for a state
        lookup by state id (stored in report)
    '''
    lookup_field = 'state_id'
    serializer_class = ReportSerializer

    def get_queryset(self):
        state_id = self.kwargs[self.lookup_field]
        return Report.objects.filter(state_id=state_id)

class SingeDayReport(generics.ListAPIView):
    '''
        Report from all states in a single day
        look up by date (year, month, day)
    '''
    lookup_fields = ['year', 'month', 'day']
    serializer_class = ReportSerializer
    queryset = Report.objects.all()

    def get_queryset(self):
        try:
            year = int(self.kwargs['year'])
            month = int(self.kwargs['month'])
            day = int(self.kwargs['day'])
            date = datetime(year=year, month=month, day=day)
            time_range = (make_aware(datetime.combine(date, time.min)),
                make_aware(datetime.combine(date, time.max)))
            return Report.objects.filter(date__range= time_range)
        except Exception as _:
            raise NotFound('Invalid date (must be yyyy/mm/dd)')

class DayRangeReport(generics.ListAPIView):
    '''
        Report from all states in a range of days
        look up by start day
        and day interval
    '''
    lookup_fields = ['year', 'month', 'day', 'day-range']
    serializer_class = ReportSerializer
    queryset = Report.objects.all()

    def get_queryset(self):
        try:
            year = int(self.kwargs['year'])
            month = int(self.kwargs['month'])
            day = int(self.kwargs['day'])
            start_day = datetime(year=year, month=month, day=day)
            end_day = start_day + timedelta(days=int(self.kwargs['day_range'])) # NOTE: currently only accepting range of 1-20 (by url matching in urls.py)
            time_range = (make_aware(datetime.combine(start_day, time.min)),
                make_aware(datetime.combine(end_day, time.max)))
            print(self.kwargs)
            return Report.objects.filter(date__range= time_range)
        except Exception as _:
            raise NotFound('Invalid date (must be yyyy/mm/dd)')
