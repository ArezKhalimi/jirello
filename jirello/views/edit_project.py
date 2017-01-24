from django.shortcuts import render
from django.http import HttpResponseRedirect

from guardian.decorators import permission_required_or_403 as perm

from .models import ProjectModel
from jirello.forms import ProjectForm


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
