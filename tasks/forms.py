    
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tasks.models import *
User._meta.get_field('email')._unique = True



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserStorieForm(forms.ModelForm):
    project = forms.ChoiceField()

    class Meta:
        model = UserStorie
        fields = ('user_story_name','total_hours_frontend_estimated','total_hours_backend_estimated','total_hours_app_estimated')
        #fields = ('user_story_name','total_hours_frontend_estimated','total_hours_backend_estimated','total_hours_app_estimated','total_hours_estimated','total_hours_frontend_worked','total_hours_backend_worked', 'total_hours_app_worked')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["project"] = forms.ChoiceField(choices=[(choice.id, choice.project_name) for choice in Project.objects.all()])


class WorkReportForm(forms.ModelForm):
    project = forms.ChoiceField()

    class Meta:
        model = WorkReport
        fields = ('hours_devoted_frontend','hours_devoted_backend','hours_devoted_app','hours_devoted_testing','notes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["project"] = forms.ChoiceField(choices=[(choice.id, choice.project_name) for choice in Project.objects.all()])


class CollaboratorsForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
    class Meta:
        model = Collaborator
        fields = ('names','last_names','email','total_salary','salary_update')

class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('project_name',)
        #fields = ('project_name','total_hours_frontend_estimated','total_hours_backend_estimated','total_hours_app_estimated','total_hours_estimated', 'total_hours_frontend_worked','total_hours_backend_worked','total_hours_app_worked')



        



