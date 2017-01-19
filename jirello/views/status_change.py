from jirello.models import Task


def status_change(request, task_id, status):
    if request.method == 'POST':
        Task.objects.filter(pk=task_id).update(status=status)
