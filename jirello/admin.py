from django.contrib import admin
from jirello.models import User
from jirello.models import ProjectModel
from jirello.models import Sprint
from jirello.models import Task
from jirello.models import Comment
from jirello.models import Worklog

admin.site.register(User)
admin.site.register(ProjectModel)
admin.site.register(Sprint)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Worklog)
