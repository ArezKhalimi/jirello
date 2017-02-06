from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def delete_btn(request, obj, projectmodel_id):
    obj.delete()
    return HttpResponseRedirect(reverse(
        'project-detail', args=[projectmodel_id, ]
    ))
