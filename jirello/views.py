from django.shortcuts import render
from jirello.models import User, Task, Sprint, ProjectModel
from jirello.forms import RegistrationForm, AuthenticationForm, ProjectForm, SprintForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login


def register(request):
    register_form = RegistrationForm()
    if request.method == 'POST':
        register_form = RegistrationForm(
            data=request.POST,
            files=request.FILES)
        if register_form.is_valid():
            register_form.save()
            new_user = auth_authenticate(
                username=register_form.cleaned_data['username'],
                password=register_form.cleaned_data['password1'],
            )
            auth_login(request, new_user)
            return HttpResponseRedirect("/jirello/")
    return render(request,
                  'jirello/register.html',
                  {'register_form': register_form})


def login(request):
    auth_form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth_authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/jirello/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse(
                "Your username and password didn't match. Please try again.")
    else:
        return render(request, 'jirello/login.html', {'auth_form': auth_form})


@login_required(login_url='/jirello/login/')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/jirello/')


def main(request):
    task_list = Task.objects.all()
    sprint_list = Sprint.objects.all()
    context_dict = {
        'task_list': task_list,
        "sprint_list": sprint_list}
    return render(request, 'jirello/main_page.html', context_dict)


def password_change(request):
    pass


@login_required(login_url='/jirello/login/')
def projects(request):
    if ProjectModel.objects.filter(users__id=request.user.id).exists():
        projects_list = ProjectModel.objects.filter(users__id=request.user.id)
    else:
        projects_list = None

    context_dict = {'projects_list': projects_list}
    return render(request, 'jirello/projects.html', context_dict)


def new_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/jirello/projects')
    context_dict = {'form': form, }
    return render(request, 'jirello/new_project.html', context_dict)


def edit_project(request, projectmodel_id):
    p = ProjectModel.objects.get_object_or_404(pk=projectmodel_id)
    form = ProjectForm(instance=p)
    if request.method == 'POST':
        form = ProjectForm(request.POST or None, instance=p)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/jirello/projects')
    # Using a new_project template
    # Bug with create new object
    return render(request, 'jirello/new_project.html', {'form': form})


def new_sprint(request, projectmodel_id):
    form = SprintForm
    if request.method == 'POST':
        form = SprintForm(request.POST)
        form.owner = request.user.id
        if form.is_valid:
            f = form.save(commit=False)
            f.owner = request.user
            f.project_id = projectmodel_id
            f.save()
            # how to redirect to new saved project???
            return HttpResponseRedirect('/jirello/projects/')
    context_dict = {'form': form, 'project_id': projectmodel_id, }
    return render(request, 'jirello/new_sprint.html', context_dict)


def edit_sprint(request, projectmodel_id):
    pass


def new_task(request):
    pass


def edit_task(request):
    pass


def projects_detail(request, projectmodel_id):
    # 404 error if project does not exist
    get_object_or_404(ProjectModel, pk=projectmodel_id)
    project = ProjectModel.objects.filter(
        pk=projectmodel_id).prefetch_related('users')
    sprints = Sprint.objects.filter(
        project_id=projectmodel_id).order_by('date_end')
    context_dict = {'project': project, 'sprints': sprints}

    if request.POST.get('delete'):
        project.delete()
    elif request.POST.get('edit'):
        return HttpResponseRedirect('/jirello/projects')
    return render(request, 'jirello/project_detail.html', context_dict)
