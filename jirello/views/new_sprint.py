from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from jirello.forms import SprintForm


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
