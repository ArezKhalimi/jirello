from datetime import datetime
import json

from django.shortcuts import render
from django.http import Http404
from django.db.models import F, Sum, Case, When, IntegerField

from guardian.decorators import permission_required_or_403 as perm

from jirello.models import ProjectModel, Task, Sprint, Worklog
from jirello.models.task_model import STATUSES
from jirello.views.status_change import status_change
from jirello.views.chart_time_left import chart_time_left
from jirello.views.chart_time_spend import chart_time_spend
from jirello.views.generate_sprint_date import generate_sprint_date


@perm('can_view', (ProjectModel, 'pk', 'projectmodel_id'))
def sprint_detail(request, projectmodel_id, sprint_id):
    # 404 error if project does not exist
    sprint = Sprint.objects.filter(pk=sprint_id)\
        .select_related('owner', 'project')\
        .annotate(sprint_original_estimate=Sum('tasks__original_estimate'))\
        .first()
    if not sprint:
        raise Http404('blabla')
    tasks = Task.objects.filter(sprints__id=sprint_id).order_by('storypoints')
    if request.method == 'POST':
        status_change(
            request,
            request.POST.get('task_id'),
            request.POST.get('status'),
        )
    total_log_time = Worklog.objects.filter(task__sprints__id=sprint_id)\
        .aggregate(Sum('time_spend')).values()
    if None not in total_log_time and sprint.tasks.exists():
        date_list = generate_sprint_date(sprint)
        annotation_kwarg = {}
        dates_kwarg = {}
        counter = 1
        annotation_kwarg['sprint_original_estimate'] = Sum(
            'tasks__original_estimate')
        for date in date_list:
            annotation_kwarg["day_{}".format(counter)] = Sum(
                Case(
                    When(
                        tasks__worklog__date_comment__range=[
                            datetime.combine(
                                sprint.date_start,
                                datetime.min.time()
                            ),
                            datetime.combine(
                                date,
                                datetime.min.time()
                            ).replace(hour=23, minute=59, second=59)
                        ],
                        then=F('tasks__worklog__time_spend')
                    ),
                    output_field=IntegerField()
                )
            )
            dates_kwarg[date] = "day_{}".format(counter)
            counter += 1
        sprint_with_dates = Sprint.objects.filter(
            pk=sprint_id).annotate(**annotation_kwarg).first()
        if sprint_with_dates:
            chart_sprint = [
                {
                    "date": str(date),
                    "duration": chart_time_left(
                        sprint_with_dates,
                        dates_kwarg,
                        date
                    ) / 60,
                    "worklog": chart_time_spend(
                        sprint_with_dates,
                        dates_kwarg,
                        date
                    ) / 60,
                }
                for date in date_list
            ]
            chart_sprint = json.dumps(chart_sprint)
        else:
            chart_sprint = None
    else:
        chart_sprint = None
    context_dict = {
        'sprint': sprint,
        'projectmodel_id': projectmodel_id,
        'tasks': tasks,
        'statuses': STATUSES,
        'chart_sprint': chart_sprint,
    }
    return render(request, 'jirello/sprint_detail.html', context_dict)
