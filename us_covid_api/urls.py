from django.urls import path, re_path
from . import views

urlpatterns = [
    # State paths
    path('states/', views.StatesDetail.as_view(), name='states-detail'),
    path('state/id/<int:id>/', views.StateDetail.as_view(), name='state-detail'),
    path('state/init/<str:initials>/', views.StateByInitials.as_view(), name='state-by-init'),
    path('state/name/<str:name>/', views.StateByName.as_view(), name='state-by-name'),
    # Report paths
    path('reports/', views.Reports.as_view(), name='reports'),
    path('global-reports/', views.GlobalReports.as_view(), name='global-reports'),
    path('state-reports/<int:state_id>/', views.StateReports.as_view(), name='state-reports'),
    re_path(
        r'date-reports/(?P<year>[12][0-9]{3})/(?P<month>1[012]|0?[1-9])/(?P<day>[12]\d|3[01]|0?[1-9]|)/$',
        views.SingeDayReport.as_view()
    ),
    re_path(
        r'date-range-reports/(?P<year>[12][0-9]{3})/(?P<month>1[012]|0?[1-9])/(?P<day>[12]\d|3[01]|0?[1-9]|)/(?P<day_range>1[0-9]|0?[1-9]|20)/$',
        views.DayRangeReport.as_view()
    ),
    # Polygon paths
    path('polygons/', views.Polygons.as_view(), name='polygons'),
    # Date
    path('start-end-date/', views.StartEndDate.as_view(), name='start-end-date'),
]
