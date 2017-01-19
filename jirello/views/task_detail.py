from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404

from guardian.decorators import permission_required_or_403 as perm

from jirello.models import ProjectModel, Task, Worklog, Comment
from jirello.models.task_model import STATUSES
from jirello.forms import WorklogForm, CommentForm
from jirello.views.status_change import status_change
from jirello.views.commit_task import commit_task


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
            return HttpResponseRedirect(reverse(
                'task_detail', args=[projectmodel_id, task_id, ]))
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
