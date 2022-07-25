from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=90, blank=True, null=True)
    total_hours_frontend_estimated = models.CharField(max_length=5, blank=True, null=True)
    total_hours_backend_estimated = models.CharField(max_length=5, blank=True, null=True)
    total_hours_app_estimated = models.CharField(max_length=5, blank=True, null=True)
    total_hours_estimated = models.CharField(max_length=5, blank=True, null=True)
    total_hours_frontend_worked = models.CharField(max_length=5, blank=True, null=True)
    total_hours_backend_worked = models.CharField(max_length=90,blank=True, null=True)
    total_hours_app_worked = models.CharField(max_length=90,blank=True, null=True)
    date_time = models.CharField(max_length=90,blank=True, null=True)

class Collaborator(models.Model):
    id = models.AutoField(primary_key=True)
    names = models.CharField(max_length=180,blank=True, null=True)
    last_names = models.CharField(max_length=180,blank=True, null=True)
    email = models.EmailField(max_length=90,blank=True, null=True)
    total_salary = models.CharField(max_length=45,blank=True, null=True)
    salary_update = models.CharField(max_length=45,blank=True, null=True)
    date_time = models.CharField(max_length=90,blank=True, null=True)
    system_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class UserStorie(models.Model):
    id = models.AutoField(primary_key=True)
    project= models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    user_story_name = models.CharField(max_length=180,blank=True, null=True)
    total_hours_frontend_estimated = models.CharField(max_length=5, blank=True, null=True)
    total_hours_backend_estimated = models.CharField(max_length=5, blank=True, null=True)
    total_hours_app_estimated = models.CharField(max_length=5, blank=True, null=True)
    total_hours_estimated = models.CharField(max_length=5, blank=True, null=True)
    total_hours_frontend_worked = models.CharField(max_length=5, blank=True, null=True)
    total_hours_backend_worked = models.CharField(max_length=90,blank=True, null=True)
    total_hours_app_worked = models.CharField(max_length=90,blank=True, null=True)
    collaborator_who_estimated = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='estimated')#usuario logueado
    collaborator_who_developed = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='developed')
    date_time = models.CharField(max_length=90,blank=True, null=True)

class WorkReport(models.Model):
    id = models.AutoField(primary_key=True)
    collaborator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)#usuario logueado
    hours_devoted_frontend = models.CharField(max_length=5, blank=True, null=True)
    hours_devoted_backend = models.CharField(max_length=5, blank=True, null=True)
    hours_devoted_app = models.CharField(max_length=5, blank=True, null=True)
    hours_devoted_testing = models.CharField(max_length=5, blank=True, null=True)
    user_story = models.ForeignKey(UserStorie, on_delete=models.CASCADE, null=True)
    entry_time = models.CharField(max_length=90,blank=True, null=True)
    project = project= models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    notes = models.TextField(blank=True, null=True)