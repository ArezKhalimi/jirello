from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from jirello.models import ProjectModel


@login_required()
def projects(request):
    if ProjectModel.objects.filter(users__id=request.user.id).exists():
        projects_list = ProjectModel.objects \
            .filter(users__id=request.user.id).order_by('title')
    else:
        projects_list = None

    context_dict = {'projects_list': projects_list}
    return render(request, 'jirello/projects.html', context_dict)
