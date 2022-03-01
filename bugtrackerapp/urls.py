from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('api/allroutes', views.allRoutes, name='allRoutes'),
]