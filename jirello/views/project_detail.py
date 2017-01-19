from django.shortcuts import render
from django.http import Http404

from guardian.decorators import permission_required_or_403 as perm

from jirello.models import ProjectModel, Sprint


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
