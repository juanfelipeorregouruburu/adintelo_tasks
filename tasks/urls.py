from django.urls import path

from tasks.views import *
from tasks import views as core_views

urlpatterns = [
    path('', core_views.login_view, name='login'),
    path('logout', core_views.salir, name='logout'),
    path('dash', Dash.as_view(), name='dash'),
    path('create_storie', core_views.createStory, name='create_storie'),
    path('stories_list/', StoriesList.as_view(), name='stories_list'),
    path('create_task', core_views.createTask, name='create_task'),
    path('tasks_list/', TasksList.as_view(), name='tasks_list'),
    path('create_collaborator', core_views.createCollaborator, name='create_collaborator'),
    path('collaborator_list/', CollaboratorList.as_view(), name='collaborator_list'),
    path('create_project', core_views.createProject, name='create_project'),
    path('project_list/', ProjectList.as_view(), name='project_list'),
]