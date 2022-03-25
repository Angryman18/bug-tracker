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
import jwt
from django.conf import settings

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


# username, passowrd, email, signedAs, technology, linkedin, github
@api_view(['POST'])
def SignUp(request):
    data = request.data
    print(make_password(data['password']))
    username = data['username']
    password = data['password']
    email = data['email']
    signedAs = data['signedAs']
    technology = data['technology']
    linkedIn = data['linkedIn']
    github = data['github']
    if (not username or not password or not email or not signedAs):
        return Response({'message': 'Please fill all the fields'}, status=status.HTTP_400_BAD_REQUEST)
    elif (User.objects.filter(username=username).exists()):
        return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    elif (User.objects.filter(email=email).exists()):
        return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            profile = UserProfile.objects.create(signedAs=signedAs, user=user, technology=technology, linkedIn=linkedIn, github=github)
            serializer = UserProfileSerializerWithToken(profile, many=False)
            return Response(serializer.data)
        except:
            return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def getAllProject(request):
    if request.method == 'POST':
        page = request.data['page']
        projects = Project.objects.all()[int(page)*1-1:int(page)*1]
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    elif request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def searchProject(request):
    inputData = request.data['slug']
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    def matchFunction(value):
        inputArr = inputData.lower().split(' ')
        finalData = list()
        for x in inputArr:
            name = value['projectName'].lower()
            desc = value['description'].lower()
            if ((x in name or x in ''.join(name.split(' '))) and x not in finalData):
                finalData.append(x)
            elif ((x in desc or x in ''.join(desc.split(' '))) and x not in finalData):
                finalData.append(x)
        return finalData
    finalData = list(filter(matchFunction, serializer.data))
    return Response(finalData, status=status.HTTP_200_OK)


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
    print(startDate, endDate)
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getUserDetails(request):
    username = request.data['username']
    try:
        userobject = User.objects.get(username=username)
        print('this is userobject', userobject)
        userProfile = UserProfile.objects.get(user=userobject)
        serializer = UserProfileSerializer(userProfile, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({'details': 'No user found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addBug(request):
    try:
        data = request.data
        title = data['title']
        description  = data['description']
        priority = data['priority']
        projectid = data['project']
        reportdate = data['reportdate']
        findProject = Project.objects.get(id=projectid)
        secretkey = request.headers['authorization'][7:]
        decoded = jwt.decode(secretkey, key=settings.SECRET_KEY, algorithms=['HS256'])
        finduser = User.objects.get(id=decoded['user_id'])
        createbug = Bug.objects.create(title=title, description=description, priority=priority, project=findProject, reportedBy=finduser, screenshot='', msg='', reportDate=reportdate)
        serializer = BugSerializer(createbug, many=False)
        return Response({'message': 'Bug added', 'data': serializer.data}, status=status.HTTP_200_OK)
    except:
        print('this is error')
        return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recentBugs(request):
    try:
        bugs = Bug.objects.all()
        last5bugs = bugs[len(bugs)-5:len(bugs)]
        serializer = BugSerializer(last5bugs, many=True)
        return Response(serializer.data.__reversed__())
    except:
        return Response({'details': 'No bug found'}, status=status.HTTP_404_NOT_FOUND)