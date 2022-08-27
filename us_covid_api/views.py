from django.http import HttpResponse
from .models import State, Report
from rest_framework import viewsets
from us_covid_api.serializers import StateSerializer, ReportSerializer


def import_data(request): #TODO: finish this
    return HttpResponse("Data should be imported")

# TODO: update these endpoints later to match needed use
class UserViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
