from dataclasses import field
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken



# NORMAL USER
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'date_joined']

class ProjectSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    def get_likes(self, obj):
        return obj.likes.count()

    class Meta:
        model = Project
        fields = '__all__'
        depth=1

# AUTHENTICATED USER
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','username', 'email', 'token','date_joined']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

# NORMAL USER PROFILE
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id','user', 'avatar', 'path', 'signedAs', 'technology', 'linkedIn','github', 'bio', 'portfolio', 'country']
        depth=1

# get logged in user profile with access token
class UserProfileSerializerWithToken(serializers.ModelSerializer):
    user = UserSerializerWithToken(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id','user', 'avatar', 'path', 'signedAs', 'technology', 'linkedIn','github','bio', 'portfolio', 'country']
        depth=1

class BugSerializer(serializers.ModelSerializer):
    reportedBy = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    class Meta:
        model = Bug
        fields = ['id','title', 'description', 'priority', 'status', 'msg', 'reportDate', 'reportedBy', 'project']
        depth=2

class FeatureSerializer(serializers.ModelSerializer):
    apealedBy = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    class Meta:
        model = FeatureRequest
        fields = '__all__'

# COMMENTS SECTION

class CommentUserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id','user', 'signedAs', 'avatar']
        depth=1


class CommentSerializer(serializers.ModelSerializer):
    user = CommentUserProfileSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'