"""geo_covid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from us_covid_api import urls as covid_api_url
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.views.static import serve 
from django.views.generic.base import RedirectView



urlpatterns = [
    path('', RedirectView.as_view(url='/doc', permanent=False), name='index'),
    path('admin/', admin.site.urls),
    path('api-auth/',include('rest_framework.urls')),
    path('api-covid/', include(covid_api_url)),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), # ! IMPORTANT For serving static files
]

# API Doc Views
urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


