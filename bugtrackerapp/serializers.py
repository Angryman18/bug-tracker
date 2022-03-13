from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken



class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

# NORMAL USER
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'date_joined', 'last_login']

# AUTHENTICATED USER
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','username', 'email', 'token','date_joined', 'last_login']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

# NORMAL USER PROFILE
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id','user', 'avatar', 'signedAs', 'technology', 'linkedIn','github']
        depth=1

# get logged in user profile with access token
class UserProfileSerializerWithToken(serializers.ModelSerializer):
    user = UserSerializerWithToken(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id','user', 'avatar', 'signedAs', 'technology', 'linkedIn','github']
        depth=1

class BugSerializer(serializers.ModelSerializer):
    reportedBy = UserSerializer(read_only=True)
    class Meta:
        model = Bug
        fields = ['id','title', 'description', 'priority', 'status', 'msg', 'reportDate', 'reportedBy', 'project']
        depth=1

