from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from guardian.shortcuts import assign_perm

from jirello.forms import ProjectForm


@login_required()
def project_new(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            # assign permissions for each user in cleaned data
            for u in form.cleaned_data['users']:
                assign_perm('can_view', u, form.instance)
                # 'delete perm' for creator
                if u == request.user:
                    assign_perm('delete_projectmodel', u, form.instance)
            return HttpResponseRedirect('/jirello/projects')
    context_dict = {'form': form, }
    return render(request, 'jirello/project_new.html', context_dict)
