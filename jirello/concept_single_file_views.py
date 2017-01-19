import json
import datetime

from django.shortcuts import render
from django.db.models import F, Sum, Case, When, IntegerField
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login

from guardian.decorators import permission_required_or_403 as perm
from guardian.shortcuts import assign_perm
from haystack.generic_views import SearchView

from .models import Task, Sprint, ProjectModel
from .models import Comment, Worklog
from .models.task_model import STATUSES
from .forms import RegistrationForm, AuthenticationForm
from .forms import ProjectForm, SprintForm, TaskForm
from .forms import CommentForm, WorklogForm


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
    return render(
        request,
        'jirello/register.html',
        {'register_form': register_form}
    )


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
                "Your username and password didn't match. Please try again."
            )
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
        projects_list = ProjectModel.objects \
            .filter(users__id=request.user.id).order_by('title')
    else:
        projects_list = None

    context_dict = {'projects_list': projects_list}
    return render(request, 'jirello/projects.html', context_dict)


def delete_btn(request, obj, projectmodel_id):
    if request.POST.get('delete'):
        obj.delete()


def status_change(request, task_id, status):
    if request.method == 'POST':
        Task.objects.filter(pk=task_id).update(status=status)


def chart_time_left(sprint, dates_kwarg, date):
    duration = sprint.sprint_original_estimate - chart_time_spend(sprint, dates_kwarg, date)
    if duration < 0:
        return 0
    return duration


def chart_time_spend(sprint, dates_kwarg, date):
    time_spend = getattr(sprint, dates_kwarg[date])
    if not time_spend:
        return 0
    return time_spend


def generate_sprint_date(sprint):
    date_list = []
    for n in range(int((sprint.date_end - sprint.date_start).days) + 1):
        date_list.append(sprint.date_start + datetime.timedelta(n))
    return date_list


def commit_task(request, form, task_id):
    if form.is_valid():
        f = form.save(commit=False)
        f.user = request.user
        f.task_id = task_id
        try:
            f.time_spend = form.cleaned_data['time_spend']
            # end of rem_est
            Task.objects.filter(pk=task_id).update(
                remaining_estimate=(F('remaining_estimate') - f.time_spend))
        except:
            f.time_spend = form.cleaned_data['time_spend']
            Task.objects.filter(pk=task_id).update(
                remaining_estimate=0)
        f.save()


@login_required()
def new_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
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
                'project_detail', args=[projectmodel_id, ]
            ))
    context_dict = {'form': form, 'project_id': projectmodel_id, }
    return render(request, 'jirello/new_sprint.html', context_dict)


@login_required()
def new_task(request, projectmodel_id):
    form = TaskForm(projectmodel_id)
    if request.method == 'POST':
        form = TaskForm(
            projectmodel_id,
            request.POST,
            user=request.user,
            project=projectmodel_id
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'project_detail', args=[projectmodel_id, ]
            ))
    context_dict = {'form': form, 'project_id': projectmodel_id, }
    return render(request, 'jirello/new_task.html', context_dict)


@perm('delete_projectmodel', (ProjectModel, 'pk', 'projectmodel_id'))
def edit_project(request, projectmodel_id):
    project = ProjectModel.objects.get(pk=projectmodel_id)
    form = ProjectForm(instance=project)
    is_creator = request.user.has_perms('projectmodel.delete_projectmodel')
    if request.method == 'POST':
        form = ProjectForm(request.POST or None, instance=project)
        if request.POST.get('delete') and is_creator:
            project.delete()
            return HttpResponseRedirect('/jirello/projects')
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/jirello/projects')
    return render(request, 'jirello/edit.html',
                  {
                      'form': form,
                      'is_creator': is_creator,
                      'project_id': projectmodel_id,
                  }
                  )


@perm('can_view', (ProjectModel, 'pk', 'projectmodel_id'))
def edit_sprint(request, projectmodel_id, sprint_id):
    sprint = Sprint.objects.get(pk=sprint_id)
    form = SprintForm(instance=sprint)
    is_creator = request.user.has_perms('projectmodel.delete_projectmodel')
    if request.method == 'POST':
        form = SprintForm(request.POST or None, instance=sprint)
        # need add perm for delete ( just for project creator)has_perms
        if is_creator:
            delete_btn(request, sprint, projectmodel_id)
            return HttpResponseRedirect(
                reverse('project_detail', args=[projectmodel_id, ]))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'sprint_detail', args=[projectmodel_id, sprint_id]
            ))
    return render(request, 'jirello/edit.html',
                  {
                      'form': form,
                      'is_creator': is_creator,
                      'project_id': projectmodel_id
                  }
                  )


@perm('can_view', (ProjectModel, 'pk', 'projectmodel_id'))
def edit_task(request, projectmodel_id, task_id):
    task = Task.objects.get(pk=task_id)
    form = TaskForm(projectmodel_id, instance=task)
    is_creator = request.user.has_perms('projectmodel.delete_projectmodel')
    if request.method == 'POST':
        form = TaskForm(projectmodel_id, request.POST or None, instance=task)
        # need add perm for delete ( just for project creator)
        if is_creator:
            delete_btn(request, task, projectmodel_id)
            return HttpResponseRedirect(reverse(
                'project_detail', args=[projectmodel_id, ]
            ))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'task_detail', args=[projectmodel_id, task_id]))
    return render(request, 'jirello/edit.html',
                  {
                      'form': form,
                      'is_creator': is_creator,
                      'project_id': projectmodel_id
                  }
                  )


@perm('can_view', (ProjectModel, 'pk', 'projectmodel_id'))
def project_detail(request, projectmodel_id):
    # 404 error if project does not exist
    try:
        project = ProjectModel.objects.filter(
            pk=projectmodel_id).prefetch_related('users', )[0]
    except project.IndexError:
        raise Http404("No project matches the given query.")
    sprints = Sprint.objects.filter(
        project_id=projectmodel_id). \
        order_by('-is_active').prefetch_related('tasks')
    context_dict = {'project': project, 'sprints': sprints}
    return render(request, 'jirello/project_detail.html', context_dict)


@perm('can_view', (ProjectModel, 'pk', 'projectmodel_id'))
def sprint_detail(request, projectmodel_id, sprint_id):
    # 404 error if project does not exist
    sprint = Sprint.objects.filter(pk=sprint_id)\
        .select_related('owner', 'project')\
        .annotate(sprint_original_estimate=Sum('tasks__original_estimate'))\
        .first()
    if not sprint:
        raise Http404('blabla')
    tasks = Task.objects.filter(sprints__id=sprint_id).order_by('storypoints')
    if request.method == 'POST':
        status_change(
            request,
            request.POST.get('task_id'),
            request.POST.get('status'),
        )
    if sprint.tasks.exists():
        date_list = generate_sprint_date(sprint)
        annotation_kwarg = {}
        dates_kwarg = {}
        counter = 1
        annotation_kwarg['sprint_original_estimate'] = Sum('tasks__original_estimate')
        for date in date_list:
            annotation_kwarg["day_{}".format(counter)] = Sum(
            Case(When(
                tasks__worklog__date_comment__range=[
                    datetime.datetime.combine(sprint.date_start,datetime.datetime.min.time()),
                    datetime.datetime.combine(date, datetime.datetime.min.time()).replace(hour=23, minute=59, second=59)
                ],
                then=F('tasks__worklog__time_spend')
                ),
                output_field=IntegerField())
            )
            dates_kwarg[date] = "day_{}".format(counter)
            counter += 1
        sprint_with_dates = Sprint.objects.filter(pk=sprint_id).annotate(**annotation_kwarg).first()

        chart_sprint = [
            {
                "date": str(date),
                "duration": chart_time_left(sprint_with_dates, dates_kwarg, date) / 60,
                "worklog": chart_time_spend(sprint_with_dates, dates_kwarg, date) / 60,
            }
            for date in date_list
        ]
        chart_sprint = json.dumps(chart_sprint)
    else:
        chart_sprint = None
    context_dict = {
        'sprint': sprint,
        'projectmodel_id': projectmodel_id,
        'tasks': tasks,
        'statuses': STATUSES,
        'chart_sprint': chart_sprint,
    }
    return render(request, 'jirello/sprint_detail.html', context_dict)


@perm('can_view', (ProjectModel, 'pk', 'projectmodel_id'))
def task_detail(request, projectmodel_id, task_id):
    # 404 error if project does not exist
    task = Task.objects.filter(pk=task_id)\
        .select_related('owner', 'project').prefetch_related('worker').first()
    if not task:
        raise Http404('blabla')
    worklogs = Worklog.objects.filter(task=task_id).order_by(
        '-date_comment').select_related('user')
    comments = Comment.objects.filter(task=task_id).order_by(
        '-date_comment').select_related('user')
    worklog_form = WorklogForm()
    comment_form = CommentForm()
    if request.method == 'POST':
        if request.POST.get('status'):
            status_change(request,
                          request.POST.get('task_id'),
                          request.POST.get('status'))
            return HttpResponseRedirect(reverse(
                'task_detail', args=[projectmodel_id, task_id, ]))
        if 'worklog' in request.POST:
            worklog_form = WorklogForm(request.POST)
            commit_task(request, worklog_form, task_id)
        elif request.POST.get('comment'):
            comment_form = CommentForm(request.POST)
            commit_task(request, comment_form, task_id)

    context_dict = {
        'comment_form': comment_form,
        'worklog_form': worklog_form,
        'task': task,
        'projectmodel_id': projectmodel_id,
        'comments': comments,
        'worklogs': worklogs,
        'statuses': STATUSES,
    }
    return render(request, 'jirello/task_detail.html', context_dict)


class TaskSearchView(SearchView):
    template_name = 'jirello/search.html'

    @method_decorator(
        perm('can_view', (ProjectModel, 'pk', 'projectmodel_id'))
    )
    def dispatch(self, *args, **kwargs):
        return super(TaskSearchView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(TaskSearchView, self).get_queryset()
        project_id = self.kwargs['projectmodel_id']
        return queryset.filter(project=project_id)
