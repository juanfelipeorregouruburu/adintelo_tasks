from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from tasks.forms import *
from tasks.models import *
from datetime import datetime
from pytz import timezone
import traceback
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm

def load_stories(request):
    project_id = request.GET.get('project')
    stories = UserStorie.objects.filter(project_id = project_id)
    return render(request, 'tasks/story_list_options.html', {'stories': stories})

def get_fecha_hora():
    fmt = "%Y-%m-%d %H:%M:%S"
    zona = 'America/Bogota'
    fecha = datetime.now(timezone(zona))
    fecha_hora = fecha.strftime(fmt)
    return fecha_hora


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dash')

    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def salir(request):
    logout(request)
    return redirect('login')

class Dash(TemplateView):
    def get(self, request):
        try:
            if request.user.is_authenticated:
                return render(request, 'tasks/dashboard.html')
            else:
                return redirect('login')
        except:
            print(traceback.format_exc())
            msg = "Error"
            return render(request, 'tasks/500.html', {"status":"error",'msg':msg}) 

@transaction.atomic
def createStory(request):   
    try:
        with transaction.atomic():
            if request.user.is_authenticated:
                if request.method == 'POST':
                    data = request.POST
                    project_id = request.POST.get('project')
                    form = UserStorieForm(request.POST)
                    if form.is_valid():
                        storie = form.save()
                        storie.date_time = get_fecha_hora()
                        storie.project_id = project_id
                        storie.collaborator_who_estimated = request.user
                        storie.total_hours_estimated = str(int(storie.total_hours_frontend_estimated) + int(storie.total_hours_backend_estimated) + int(storie.total_hours_app_estimated))
                        storie.save()
                        form = UserStorieForm()
                        msg = "La historia de usuario se creó correctamente"
                        return render(request, 'tasks/create_storie.html', {'form': form, "status":"ok",'msg':msg}) 
                    else:
                        print('Formulario no valido')
                else:              
                    form = UserStorieForm()
                    return render(request, 'tasks/create_storie.html', {'form': form}) 
            else:
                return redirect('login')
    except:
        print(traceback.format_exc())
        msg = "Error"
        return render(request, 'tasks/500.html', {"status":"error",'msg':msg}) 

class StoriesList(TemplateView):
    def get(self, request):
        try:
            if request.user.is_authenticated:
                stories = UserStorie.objects.all()
                return render(request, 'tasks/stories_list.html', {'stories':stories})
            else:
                return redirect('login')
        except:
            print(traceback.format_exc())
            msg = "Error"
            return render(request, 'tasks/500.html', {"status":"error",'msg':msg}) 


@transaction.atomic
def createTask(request):   
    try:
        with transaction.atomic():
            if request.user.is_authenticated:
                if request.method == 'POST':
                    data = request.POST
                    project_id = request.POST.get('project')
                    storie_id = data['id_story']
                    form = WorkReportForm(request.POST)
                    if form.is_valid():
                        task = form.save()
                        task.entry_time = get_fecha_hora()
                        task.project_id = project_id
                        task.user_story_id = storie_id
                        task.collaborator = request.user
                        task.save()
                        story = UserStorie.objects.get(id=storie_id)
                        story.total_hours_frontend_worked = str(int(story.total_hours_frontend_worked) + int(task.hours_devoted_frontend))
                        story.total_hours_backend_worked = str(int(story.total_hours_backend_worked) + int(task.hours_devoted_backend))
                        story.total_hours_app_worked = str(int(story.total_hours_app_worked) + int(task.hours_devoted_app))
                        story.save()
                        form = WorkReportForm()
                        msg = "La tarea se creó correctamente"
                        return render(request, 'tasks/create_task.html', {'form': form, "status":"ok",'msg':msg}) 
                    else:
                        print('Formulario no valido')
                else:              
                    form = WorkReportForm()
                    return render(request, 'tasks/create_task.html', {'form': form}) 
            else:
                return redirect('login')
    except:
        print(traceback.format_exc())
        msg = "Error"
        return render(request, 'tasks/500.html', {"status":"error",'msg':msg}) 

class TasksList(TemplateView):
    def get(self, request):
        try:
            if request.user.is_authenticated:
                tasks = WorkReport.objects.all()
                return render(request, 'tasks/tasks_list.html', {'tasks':tasks})
            else:
                return redirect('login')
        except:
            print(traceback.format_exc())
            msg = "Error"
            return render(request, 'tasks/500.html', {"status":"error",'msg':msg}) 

@transaction.atomic
def createCollaborator(request):   
    try:
        with transaction.atomic():
            if request.user.is_authenticated and request.user.is_superuser:
                if request.method == 'POST':
                    data = request.POST
                    password = request.POST.get('password')
                    username = request.POST.get('username')
                    form = CollaboratorsForm(request.POST)
                    if form.is_valid():
                        collaborator = form.save()
                        system_user = User(username=username,email=collaborator.email)
                        system_user.set_password(password)
                        system_user.save()
                        collaborator.date_time = get_fecha_hora()
                        collaborator.system_user = system_user
                        collaborator.save()
                        form = CollaboratorsForm()
                        msg = "El colaborador se creó correctamente"
                        return render(request, 'tasks/create_collaborator.html', {'form': form, "status":"ok",'msg':msg}) 
                    else:
                        print('Formulario no valido')
                else:              
                    form = CollaboratorsForm()
                    return render(request, 'tasks/create_collaborator.html', {'form': form}) 
            else:
                return redirect('login')
    except:
        print(traceback.format_exc())
        msg = "Error"
        return render(request, 'tasks/500.html', {"status":"error",'msg':msg}) 

class CollaboratorList(TemplateView):
    def get(self, request):
        try:
            if request.user.is_authenticated and request.user.is_superuser:
                collaborators = Collaborator.objects.all()
                return render(request, 'tasks/collaborators_list.html', {'collaborators':collaborators})
            else:
                return redirect('login')
        except:
            print(traceback.format_exc())
            msg = "Error"
            return render(request, 'tasks/500.html', {"status":"error",'msg':msg}) 

@transaction.atomic
def createProject(request):   
    try:
        with transaction.atomic():
            if request.user.is_authenticated and request.user.is_superuser:
                if request.method == 'POST':
                    data = request.POST
                    form = ProjectsForm(request.POST)
                    if form.is_valid():
                        project = form.save()
                        project.date_time = get_fecha_hora()
                        project.save()
                        form = ProjectsForm()
                        msg = "El proyecto se creó correctamente"
                        return render(request, 'tasks/create_project.html', {'form': form, "status":"ok",'msg':msg}) 
                    else:
                        print('Formulario no valido')
                else:              
                    form = ProjectsForm()
                    return render(request, 'tasks/create_project.html', {'form': form}) 
            else:
                return redirect('login')
    except:
        print(traceback.format_exc())
        msg = "Error"
        return render(request, 'tasks/500.html', {"status":"error",'msg':msg}) 

class ProjectList(TemplateView):
    def get(self, request):
        try:
            if request.user.is_authenticated and request.user.is_superuser:
                projects = Project.objects.all()
                return render(request, 'tasks/projects_list.html', {'projects':projects})
            else:
                return redirect('login')
        except:
            print(traceback.format_exc())
            msg = "Error"
            return render(request, 'tasks/500.html', {"status":"error",'msg':msg}) 
