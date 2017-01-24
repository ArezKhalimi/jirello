from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from guardian.decorators import permission_required_or_403 as perm

from jirello.models import ProjectModel, Sprint
from jirello.forms import SprintForm
from jirello.views.delete_btn import delete_btn


@perm('can_view', (ProjectModel, 'pk', 'projectmodel_id'))
def edit_sprint(request, projectmodel_id, sprint_id):
    sprint = Sprint.objects.get(pk=sprint_id)
    form = SprintForm(instance=sprint)
    is_creator = request.user.has_perms('projectmodel.delete_projectmodel')
    if request.method == 'POST':
        form = SprintForm(request.POST or None, instance=sprint)
        # need add perm for delete ( just for project creator)has_perms
        if is_creator and request.POST.get('delete'):
            return delete_btn(request, sprint, projectmodel_id)
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
