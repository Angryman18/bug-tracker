from datetime import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth.hashers import make_password
# Models
from .models import Project, Comment, Bug, FeatureRequest, UserProfile
from django.db.models import Q
# Serializers
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import jwt
from django.conf import settings

# helpers
from .helper import getLoggedInUserDetail, checkIfDeveloper

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
        projects = Project.objects.all().order_by("-id")[int(page)*4-4:int(page)*4]
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    elif request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data.__reversed__())

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addProject(request):
    data = request.data
    projectName = data['projectName']
    description = data['description']
    githubLink = data['githubLink']
    liveSiteLink = data['liveSiteLink']
    user = getLoggedInUserDetail(request.headers)
    if (not projectName or not description or not githubLink or not liveSiteLink):
        return Response({'message': 'Please fill all the fields'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            if (checkIfDeveloper(request.headers)):
                project = Project.objects.create(user=user, projectName=projectName, description=description, githubLink=githubLink, liveSiteLink=liveSiteLink)
                serializer = ProjectSerializer(project, many=False)
                return Response(serializer.data)
            else:
                return Response({'message': 'This isnt a Developer Account. Only Developer can add Projects.'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def searchProject(request):
    inputData = request.data['slug']
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    def matchFunction(value):
        inputArr = inputData.lower().split(' ')
        for x in inputArr:
            name = value['projectName'].lower()
            desc = value['description'].lower()
            if (x in name or x in ''.join(name.split(' '))):
                return {"priority": "title", "data": value}
            elif (x in desc or x in ''.join(desc.split(' '))):
                return {"priority": "desc", "data": value}
            else:
                return {"priority": "none", "data": None}
    finalData = list()
    for x in list(map(matchFunction, serializer.data)):
        if x["priority"] == "title":
            finalData.insert(0, x["data"])
        elif x["priority"] == "desc":
            finalData.append(x["data"])
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
        finduser = getLoggedInUserDetail(request.headers)
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
        if (len(bugs) > 5):
            last5bugs = bugs[len(bugs)-5:len(bugs)]
            serializer = BugSerializer(last5bugs, many=True)
            return Response(serializer.data.__reversed__())
        else:
            last5bugs = bugs[0:len(bugs)]
            serializer = BugSerializer(last5bugs, many=True)
            return Response(serializer.data.__reversed__())
    except:
        return Response({'details': 'No bug found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getUserSpeceficContent(request):
    try:
        finduser = getLoggedInUserDetail(request.headers)
        user_Serializer = UserSerializer(finduser, many=False)
        userProfile = UserProfile.objects.get(user=finduser)
        bugSerializer = None
        featureSerializer = None
        if (userProfile.signedAs == "Developer"):
            getAllBugs = Bug.objects.filter(Q(project__user__id=user_Serializer.data["id"]) | Q(reportedBy__id=user_Serializer.data["id"])).order_by('-id')
            getAllFeatures = FeatureRequest.objects.filter(Q(project__user__id=user_Serializer.data["id"]) | Q(apealedBy__id=user_Serializer.data["id"])).order_by('-id')
            featureSerializer = FeatureSerializer(getAllFeatures, many=True)
            bugSerializer = BugSerializer(getAllBugs, many=True)
        else:
            getAllBugs = Bug.objects.filter(reportedBy__id=user_Serializer.data["id"]).order_by('-id')
            getAllFeatures = FeatureRequest.objects.filter(apealedBy__id=user_Serializer.data["id"]).order_by('-id')
            featureSerializer = FeatureSerializer(getAllFeatures, many=True)
            bugSerializer = BugSerializer(getAllBugs, many=True)
        resp = {"bugs": bugSerializer.data, "features": featureSerializer.data}
        return Response(resp, status=status.HTTP_200_OK)
    except:
        return Response({'details': 'No bug found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateBugs(request):
    try:
        msg = request.data['msg']
        bug_status = request.data['status']
        bugid = request.data['bugid']
        findBug = Bug.objects.get(id=bugid)
        ownerId = findBug.get_project_user_id() # get user id of the project owner
        user = getLoggedInUserDetail(request.headers) # get logged in user
        profile = UserProfile.objects.get(user=user) # get logged in user profile
        if (profile.signedAs != 'Developer'):
            return Response({'message': 'You are not authorized to update the bug'}, status=status.HTTP_401_UNAUTHORIZED)
        elif (ownerId != user.id):
            return Response({'message': 'You are not Owner of the Project'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            findBug.msg = msg
            findBug.status = bug_status
            findBug.save()
            return Response({'message': 'Bug Updated Successfully!'}, status=status.HTTP_200_OK)   
    except:
        return Response({'message': 'Sorry Something Error Occured'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateFeatures(request):
    try:
        user = getLoggedInUserDetail(request.headers)
        msg = request.data['msg']
        featureStatus = request.data['status']
        id = request.data['id']
        findFeature = FeatureRequest.objects.get(id=id)
        findOwner = findFeature.get_project_user_id()
        profile = UserProfile.objects.get(user=user)
        if (profile.signedAs != 'Developer'):
            return Response({'message': 'You are not authorized to update the feature'}, status=status.HTTP_401_UNAUTHORIZED)
        elif (findOwner != user.id):
            return Response({'message': 'You are not Owner of the Project'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            findFeature.msg = msg
            findFeature.status = featureStatus
            findFeature.save()
            return Response({'message': 'Feature Updated Successfully!'}, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'Sorry Something Error Occured'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteFeature(request):
    try:
        id = request.data['id']
        user = getLoggedInUserDetail(request.headers)
        profile = UserProfile.objects.get(user=user)
        if (profile.signedAs != 'Developer'):
            return Response({'message': 'You are not authorized to delete the feature'}, status=status.HTTP_401_UNAUTHORIZED)
        feature = FeatureRequest.objects.get(id=id)
        feature.delete()
        return Response({'message': 'Feature Deleted Successfully!'}, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'Sorry Something Error Occured'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteBug(request):
    try:
        id = request.data['id']
        user = getLoggedInUserDetail(request.headers)
        profile = UserProfile.objects.get(user=user)
        if (profile.signedAs != 'Developer'):
            return Response({'message': 'You are not authorized to delete the bug'}, status=status.HTTP_401_UNAUTHORIZED)
        bug = Bug.objects.get(id=id)
        bug.delete()
        return Response({'message': 'Bug Deleted Successfully!'}, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'Sorry Something Error Occured'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allFeatures(request):
    try:
        features = FeatureRequest.objects.all()
        serializer = FeatureSerializer(features, many=True)
        return Response(serializer.data.__reversed__())
    except:
        return Response({'details': 'No data found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addFeatures(request):
    try:
        data = request.data
        title = data['title']
        description  = data['description']
        project = data['project']
        apealdate = data['apealdate']
        user = getLoggedInUserDetail(request.headers)
        getProject = Project.objects.get(id=int(project))
        FeatureRequest.objects.create(title=title, description=description, project=getProject, apealDate=apealdate, apealedBy=user)
        return Response({'message': 'Feature added'}, status=status.HTTP_200_OK)
    except:
        return Response({'details': 'Error Adding Feature'}, status=status.HTTP_404_NOT_FOUND)

# COMMETNS API

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def commentOnProject(request):
    try:
        user = getLoggedInUserDetail(request.headers)
        profile = UserProfile.objects.get(user=user)
        comment = request.data['comment']
        projectId = request.data['projectId']
        project = Project.objects.get(id=int(projectId))
        Comment.objects.create(user=profile, comment=comment, project=project, commentDate=datetime.now())
        return Response({'message': 'Comment is added'}, status=status.HTTP_200_OK)
    except:
        return Response({'details': 'Error Adding Comment'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProjectBasedComments(request, projectId):
    try:
        getAllComments = Comment.objects.filter(project__id=projectId).order_by('-id')
        serializer = CommentSerializer(getAllComments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({'details': 'No Comment Added'}, status=status.HTTP_404_NOT_FOUND)

# LIKES API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addLikeOnProject(request):
    try:
        projectId = request.data['projectId']
        user = getLoggedInUserDetail(request.headers)
        findProject = Project.objects.get(id=int(projectId))
        if (findProject.likes.filter(id=user.id).exists()):
            findProject.likes.remove(user)
            return Response({'message': 'Disliked'}, status=status.HTTP_200_OK)
        findProject.likes.add(user)
        totalLike = findProject.total_likes()
        return Response({'message': 'Liked'}, status=status.HTTP_200_OK)
    except:
        pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def editProfile(request):
    try:
        data = request.data
        technology = data['technology']
        github = data['github']
        linkedin = data['linkedIn']
        bio = data['bio']
        country = data['country']
        portfolio = data['portfolio']
        avatar = data.get('avatar')
        path = data.get('path')
        user = getLoggedInUserDetail(request.headers)
        profile = UserProfile.objects.get(user=user)
        profile.technology = technology
        profile.github = github
        profile.linkedIn = linkedin
        profile.bio = bio
        profile.country = country
        profile.portfolio = portfolio
        if (avatar != None and path != None):
            profile.avatar = avatar
            profile.path = path
        profile.save()
        profileSerializer = UserProfileSerializer(profile, many=False)
        return Response(profileSerializer.data, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'Sorry Something Error Occured'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getDashboardStats(request):
    try:
        user = getLoggedInUserDetail(request.headers)
        totDev = UserProfile.objects.filter(signedAs="Developer")
        totUsr = UserProfile.objects.filter(signedAs="User")
        totTst = UserProfile.objects.filter(signedAs="Tester")

        totBug = Bug.objects.all().count()
        totProject = Project.objects.all().count()
        totFeat = FeatureRequest.objects.all().count()
        totCom = Comment.objects.all().count()

        resolveBug = Bug.objects.filter(status="Resolved").count()
        pendingBug = Bug.objects.filter(status="Pending").count()
        rejectBug = Bug.objects.filter(status="Rejected").count()
        inProgressBug = Bug.objects.filter(status="In Progress").count()

        Unverified = FeatureRequest.objects.filter(status="Unverified").count()
        pendingFeat = FeatureRequest.objects.filter(status="in Talk").count()
        rejectFeat = FeatureRequest.objects.filter(status="Rejected").count()
        acceptedFeature = FeatureRequest.objects.filter(status="Accepted").count()

        userData = {'totalDev': totDev.count(), 'totalUsr': totUsr.count(), 'totalTst': totTst.count()}
        dataStats = {'totalBug': totBug, "totalProjects": totProject, 'totalFeat': totFeat, 'totalCom': totCom}
        bugData = {'totalBug': totBug, 'resolveBug': resolveBug, 'pendingBug': pendingBug, 'rejectBug': rejectBug, 'inProgressBug': inProgressBug}
        featData = {'totalFeat': totFeat, 'Unverified': Unverified, 'inTalkFeature': pendingFeat, "AcceptedFeature": acceptedFeature, 'rejectFeat': rejectFeat}

        return Response({"userData": userData, "data_stats": dataStats, "bugData": bugData, "featData": featData}, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'Sorry Something Error Occured'}, status=status.HTTP_404_NOT_FOUND)
