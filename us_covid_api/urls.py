from django.urls import path, re_path
from . import views

urlpatterns = [
    path('states/', views.StatesDetail.as_view(), name='states-detail'),
    path('state/<int:id>/', views.StateDetail.as_view(), name='state-detail'),
    path('reports/', views.Reports.as_view(), name='reports'),
    path('state-reports/<int:state_id>/', views.StateReports.as_view(), name='state-reports'),
    re_path(
        r'date-reports/(?P<year>[12][0-9]{3})/(?P<month>1[012]|0?[1-9])/(?P<day>[12]\d|3[01]|0?[1-9]|)/$',
        views.SingeDayReport.as_view()
    ),
    re_path(
        r'date-range-reports/(?P<year>[12][0-9]{3})/(?P<month>1[012]|0?[1-9])/(?P<day>[12]\d|3[01]|0?[1-9]|)/(?P<day_range>1[0-9]|0?[1-9]|20)/$',
        views.DayRangeReport.as_view()
    ),
]
