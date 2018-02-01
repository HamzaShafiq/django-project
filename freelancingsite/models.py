from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

USER_ROLES = {'freelancer': 'freelancer', 'recruiter': 'recruiter'}

USER_CHOICES = [
    (USER_ROLES['freelancer'], "I'm a Freelancer"),
    (USER_ROLES['recruiter'], "I'm a Recruiter"),
]


class User(AbstractUser):
    user_role = models.CharField(max_length=100, choices=USER_CHOICES, default='freelancer')

    def __str__(self):
        return self.username


class Project(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=10)
    assigned_to = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ProjectBid(models.Model):
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_bids')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='bids')
    amount = models.FloatField()

    def __str__(self):
        return self.project.name

