from . import views
from django.urls import path
from .views import MyTokenObtainPairView


urlpatterns = [
    path('user/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/signup', views.SignUp, name='signup'),
    path('home', views.Home, name='home'),
    path('projects', views.getAllProject, name='projects'),
    path('bugs', views.getAllBugs, name='bugs'),
    path('findUser', views.getUserDetail, name='findUser'),
    path('users', views.getAllUserProfile, name='users'),
    path('filterBugDateRange', views.filterBugDateRange, name='filterBugDateRange'),
    path('getuserdetail', views.getUserDetails, name='getuserdetail'),
    path('addbug', views.addBug, name='addbug'),
]