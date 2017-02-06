from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from guardian.decorators import permission_required_or_403 as perm

from jirello.models import ProjectModel, Task
from jirello.forms import TaskForm
from jirello.views.delete_btn import delete_btn


@perm('can_view', (ProjectModel, 'pk', 'projectmodel_id'))
def task_edit(request, projectmodel_id, task_id):
    task = Task.objects.get(pk=task_id)
    form = TaskForm(projectmodel_id, instance=task)
    is_creator = request.user.has_perms('projectmodel.delete_projectmodel')
    if request.method == 'POST':
        form = TaskForm(projectmodel_id, request.POST or None, instance=task)
        # need add perm for delete ( just for project creator)
        if is_creator and request.POST.get('delete'):
            return delete_btn(request, task, projectmodel_id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'task-detail', args=[projectmodel_id, task_id]))
    return render(request, 'jirello/edit.html',
                  {
                      'form': form,
                      'is_creator': is_creator,
                      'project_id': projectmodel_id
                  }
                  )
