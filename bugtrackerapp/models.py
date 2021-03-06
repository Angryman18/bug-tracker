from pickle import NONE
from pyexpat import model
from secrets import choice
from tokenize import triple_quoted
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
# Create your models here.


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    projectName = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='thumbnail',null=True, blank=True)
    uploadData = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    githubLink = models.URLField(max_length=200, null=True, blank=True, validators=[URLValidator])
    liveSiteLink = models.URLField(max_length=200, null=True, blank=True)
    contributers = models.JSONField(null=True, blank=True)
    message = models.CharField(max_length=200, null=True, blank=True)
    recruiting = models.BooleanField(default=False, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True, null=True)

    def __str__(self):
        return self.projectName
    
    def total_likes(self):
        return self.likes.count()

class Bug(models.Model):
    PRIORITY_CHOICES =(
    ("High", "High"),
    ("Medium", "Medium"),
    ("Low", "Low"),
    ("Unknown", "Unknown"),
    )

    STATUS_CHOICES =(
    ("Pending", "Pending"),
    ("In Progress", "In Progress"),
    ("Resolved", "Resolved"),
    ("Rejected", "Rejected"),
    )
    reportedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    screenshot = models.ImageField(upload_to='bug-screenshot',null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=50, default="Low", null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default="Pending", null=True, blank=True)
    msg = models.TextField(max_length=200, null=True, blank=True)
    reportDate = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.title} - {self.project}'

    def get_project_user_id(self):
        return self.project.user.id # to reflect some data or do calculation from the model field
        # project => user => id


class FeatureRequest(models.Model):
    STATUS_CHOICES =(
    ("Unverified", "Unverified"),
    ("in Talk", "in Talk"),
    ("Accepted", "Accepted"),
    ("Rejected", "Rejected"),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    apealedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    msg = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    apealDate = models.DateField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=50, choices= STATUS_CHOICES, default="Unverified", null=True, blank=True)

    def __str__(self):
        return f'{self.title} - {self.project}'

    def get_project_user_id(self):
        return self.project.user.id


class UserProfile(models.Model):
    ROLE = (
        ("Developer", "Developer"),
        ("Tester", "Tester"),
        ('User', 'User')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    avatar = models.URLField(max_length=500, null=True, blank=True)
    path = models.CharField(max_length=200, null=True, blank=True)
    signedAs = models.CharField(max_length=200, choices=ROLE, default='User', null=True, blank=True)
    technology = models.CharField(max_length=200, null=True, blank=True)
    linkedIn = models.URLField(max_length=200, null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    portfolio = models.URLField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)



    def __str__(self):
        return f'{self.signedAs} - {str(self.user)}'

class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    commentDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.comment}'