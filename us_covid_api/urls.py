from django.urls import path, include
from . import views
from rest_framework import routers

# Why? https://www.django-rest-framework.org/tutorial/quickstart/#urls
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('import-data', views.import_data, name='import-data'),
]
