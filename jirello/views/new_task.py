from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from jirello.forms import TaskForm


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
