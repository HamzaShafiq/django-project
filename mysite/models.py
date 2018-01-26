from django.db import models
from django.contrib.auth.models import AbstractUser

USER_CHOICES = [
    ('freelancer', "I'm a Freelancer"),
    ('recruiter', "I'm a Recruiter"),
    ]


class User(AbstractUser):
    user_role = models.CharField(max_length=100, choices=USER_CHOICES, default='freelancer')


class Project(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=30)
    assigned_to = models.CharField(max_length=30)


class ProjectBid(models.Model):
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.FloatField()