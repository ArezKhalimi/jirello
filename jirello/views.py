from django.shortcuts import render
from jirello.models import User, Task, Sprint, ProjectModel
from jirello.forms import RegistrationForm, AuthenticationForm
from jirello.forms import ProjectForm, SprintForm, TaskForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from guardian.decorators import permission_required_or_403
from guardian.shortcuts import assign_perm


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
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse(
                "Your username and password didn't match. Please try again.")
    else:
        return render(request, 'jirello/login.html', {'auth_form': auth_form})


@login_required()
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/jirello/')


def main(request):
    return render(request, 'jirello/main_page.html')


def password_change(request):
    pass


@login_required()
def projects(request):
    if ProjectModel.objects.filter(users__id=request.user.id).exists():
        projects_list = ProjectModel.objects.filter(users__id=request.user.id)
    else:
        projects_list = None

    context_dict = {'projects_list': projects_list}
    return render(request, 'jirello/projects.html', context_dict)


@login_required()
def new_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid:
            form.save()
            # assign permissions for each user in cleaned data
            for u in form.cleaned_data['users']:
                assign_perm('can_view', u, form.instance)
                # delete perm for creator
                if u == request.user:
                    assign_perm('delete_projectmodel', u, form.instance)
            return HttpResponseRedirect('/jirello/projects')
    context_dict = {'form': form, }
    return render(request, 'jirello/new_project.html', context_dict)


@login_required()
def new_sprint(request, projectmodel_id):
    form = SprintForm
    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user
            f.project_id = projectmodel_id
            f.save()
            return HttpResponseRedirect(reverse(
                'project_detail', args=[projectmodel_id, ]))
    context_dict = {'form': form, 'project_id': projectmodel_id, }
    return render(request, 'jirello/new_sprint.html', context_dict)


@login_required()
def new_task(request, projectmodel_id):
    form = TaskForm()
    # query workers, sprints and parrent of project
    form.fields["worker"].queryset = User.objects.filter(
        projects__id=projectmodel_id).prefetch_related('projects')
    form.fields["sprints"].queryset = Sprint.objects.filter(
        project_id=projectmodel_id).order_by('date_end')
    form.fields["parent"].queryset = Task.objects.filter(
        project_id=projectmodel_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user,
                        project=projectmodel_id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'project_detail', args=[projectmodel_id, ]))
    context_dict = {'form': form, 'project_id': projectmodel_id, }
    return render(request, 'jirello/new_task.html', context_dict)


@permission_required_or_403('delete_projectmodel',
                            (ProjectModel, 'pk', 'projectmodel_id'))
def edit_project(request, projectmodel_id):
    project = ProjectModel.objects.get(pk=projectmodel_id)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST or None, instance=project)
        if request.POST.get('delete'):
            project.delete()
            return HttpResponseRedirect('/jirello/projects')
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/jirello/projects')
    return render(request, 'jirello/edit.html', {'form': form})


def delete_btn(request, obj, projectmodel_id):
    if request.POST.get('delete'):
        obj.delete()
        return HttpResponseRedirect(
            reverse('project_detail', args=[projectmodel_id, ]))


@permission_required_or_403('can_view',
                            (ProjectModel, 'pk', 'projectmodel_id'))
def edit_sprint(request, projectmodel_id, sprint_id):
    sprint = Sprint.objects.get(pk=sprint_id)
    form = SprintForm(instance=sprint)
    is_creator = request.user.has_perms('projectmodel.delete_projectmodel')
    if request.method == 'POST':
        form = SprintForm(request.POST or None, instance=sprint)
        # need add perm for delete ( just for project creator)has_perms
        if is_creator:
            delete_btn(request, sprint, projectmodel_id)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'sprint_detail', args=[projectmodel_id, sprint_id]))
    return render(request, 'jirello/edit.html',
                  {'form': form, 'is_creator': is_creator, })


@permission_required_or_403('can_view',
                            (ProjectModel, 'pk', 'projectmodel_id'))
def edit_task(request, projectmodel_id, task_id):
    task = Task.objects.get(pk=task_id)
    form = TaskForm(instance=task)
    is_creator = request.user.has_perms('projectmodel.delete_projectmodel')
    if request.method == 'POST':
        form = TaskForm(request.POST or None, instance=task)
        # need add perm for delete ( just for project creator)
        if is_creator:
            delete_btn(request, task, projectmodel_id)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'task_detail', args=[projectmodel_id, task_id]))
    return render(request, 'jirello/edit.html',
                  {'form': form, 'is_creator': is_creator, })


@permission_required_or_403('can_view',
                            (ProjectModel, 'pk', 'projectmodel_id'))
def project_detail(request, projectmodel_id):
    # 404 error if project does not exist
    try:
        project = ProjectModel.objects.filter(
            pk=projectmodel_id).prefetch_related('users', )[0]
    except project.IndexError:
        raise Http404("No project matches the given query.")
    sprints = Sprint.objects.filter(
        project_id=projectmodel_id).order_by('-is_active').prefetch_related('tasks')
    context_dict = {'project': project, 'sprints': sprints}
    return render(request, 'jirello/project_detail.html', context_dict)


@permission_required_or_403('can_view',
                            (ProjectModel, 'pk', 'projectmodel_id'))
def sprint_detail(request, projectmodel_id, sprint_id):
    # 404 error if project does not exist
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    tasks = Task.objects.filter(sprints__id=sprint_id).order_by('storypoints')
    context_dict = {'sprint': sprint,
                    'projectmodel_id': projectmodel_id, 'tasks': tasks}
    return render(request, 'jirello/sprint_detail.html', context_dict)


@permission_required_or_403('can_view',
                            (ProjectModel, 'pk', 'projectmodel_id'))
def task_detail(request, projectmodel_id, task_id):
    # 404 error if project does not exist
    task = get_object_or_404(Task, pk=task_id)
    context_dict = {'task': task, 'projectmodel_id': projectmodel_id}
    return render(request, 'jirello/task_detail.html', context_dict)
