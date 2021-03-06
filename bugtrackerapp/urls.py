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
    path('recent-bugs', views.recentBugs, name='recent-bugs'),
    path('search-project', views.searchProject, name='search-project'),
    path('add-project', views.addProject, name='add-project'),
    path('get-userspecefic-content', views.getUserSpeceficContent, name='get-user-bugs'),
    path('update-bug', views.updateBugs, name='update-bug'),
    path('updateFeatures', views.updateFeatures, name='updateFeatures'),
    path('deleteFeature', views.deleteFeature, name='deleteFeature'),
    path('deleteBug', views.deleteBug, name='deleteBug'),
    path('allfeatures', views.allFeatures, name='allfeatures'),
    path('add-feature', views.addFeatures, name='add-features'),

    path('add-comment-on-project', views.commentOnProject, name='add-comment'),
    path('get-projects-comments/<int:projectId>', views.getProjectBasedComments, name='get-projects-comments'),

    path("add-like", views.addLikeOnProject, name="add-like"),

    path('editProfile', views.editProfile, name='editProfile'),

    path('getDashboardStats', views.getDashboardStats, name='getDashboardStats'),
]