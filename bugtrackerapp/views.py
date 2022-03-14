from datetime import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth.hashers import make_password
# Models
from .models import Project, Comment, Bug, FeatureRequest, UserProfile
# Serializers
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def Home(request):
    return Response({'message': 'Hello World'})


@api_view(['POST'])
def SignUp(request):
    data = request.data
    print(data['password'])
    print(make_password(data['password']))
    user = User.objects.create_user(username=data['username'], password=data['password'], email=data['email'])
    profile = UserProfile.objects.create(signedAs=data['signedAs'], user=user, technology=data['technology'], linkedIn=data['linkedIn'], github=data['github'])
    serializer = UserProfileSerializerWithToken(profile, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getAllProject(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes(([IsAuthenticated]))
def getAllBugs(request):
    bugs = Bug.objects.all()
    serializer = BugSerializer(bugs, many=True)
    return Response(serializer.data.__reversed__())

@api_view(['POST'])
def getUserDetail(request):
    try:
        id = request.data['id']
        user = User.objects.get(id=id)
        findProfile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(findProfile, many=False)
        return Response(serializer.data)
    except:
        return Response({"details": "user not found"}, status=status.HTTP_404_NOT_FOUND)

# "startDate": "2022-03-11",
# "endDate": "2022-03-11"
@api_view(['POST'])
@permission_classes(([IsAuthenticated]))
def filterBugDateRange(request):
    startDate = request.data['startDate']
    endDate = request.data['endDate']
    startDate = datetime.strptime(startDate, '%Y-%m-%d')
    endDate = datetime.strptime(endDate, '%Y-%m-%d')
    bugs = Bug.objects.filter(reportDate__range=[startDate, endDate])
    serializer = BugSerializer(bugs, many=True)
    return Response(serializer.data.__reversed__())

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllUserProfile(request):
    try:
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)
    except:
        return Response({'details': 'No user found'}, status=status.HTTP_404_NOT_FOUND)