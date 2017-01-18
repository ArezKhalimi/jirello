from haystack import indexes

from jirello.models import Task


class TaskIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField()
    description = indexes.CharField()
    project = indexes.IntegerField(model_attr='project_id')

    def get_model(self):
        return Task

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
