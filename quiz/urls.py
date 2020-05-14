from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
app_name = 'quiz'

urlpatterns = [
    #path('api/', include(router.urls)),
    path('', views.HomeView, name='home'),
]
