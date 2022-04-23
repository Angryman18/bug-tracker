import jwt 
from django.conf import settings
from django.contrib.auth.models import User

from .serializers import *
from .models import UserProfile

def userFinder(userData, serializedData):
    for user in serializedData:
        pass
    return None

def getLoggedInUserDetail(secretKey):
    secretkey = secretKey['authorization'][7:]
    decoded = jwt.decode(secretkey, key=settings.SECRET_KEY, algorithms=['HS256'])
    finduser = User.objects.get(id=decoded['user_id'])
    return finduser

def checkIfDeveloper(secretKey):
    getUser = getLoggedInUserDetail(secretKey)
    findUser = UserProfile.objects.get(user__id=getUser.id)
    return findUser.signedAs == 'Developer'
