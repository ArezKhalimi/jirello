from django.utils.decorators import method_decorator

from haystack.generic_views import SearchView
from guardian.decorators import permission_required_or_403 as perm
from jirello.models import ProjectModel


class TaskSearchView(SearchView):
    template_name = 'jirello/search.html'

    @method_decorator(
        perm('can_view', (ProjectModel, 'pk', 'projectmodel_id'))
    )
    def dispatch(self, *args, **kwargs):
        return super(TaskSearchView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(TaskSearchView, self).get_queryset()
        project_id = self.kwargs['projectmodel_id']
        return queryset.filter(project=project_id)
