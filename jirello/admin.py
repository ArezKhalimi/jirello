from django.contrib import admin
from jirello.models import User
from jirello.models import ProjectModel
from jirello.models import Sprint


admin.site.register(User)
admin.site.register(ProjectModel)
admin.site.register(Sprint)
