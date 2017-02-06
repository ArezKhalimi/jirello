from django.db.models import F

from jirello.models import Task


def task_commit(request, form, task_id):
    if form.is_valid():
        f = form.save(commit=False)
        f.user = request.user
        f.task_id = task_id
        # Change remaining estimate comparable with adding worklog time.
        if hasattr(f, 'time_spend'):
            f.time_spend = form.cleaned_data['time_spend']
            try:
                Task.objects.filter(pk=task_id).update(
                    remaining_estimate=(F('remaining_estimate') - f.time_spend))
            # Remaing estimate can`t be negative. Because of that after time
            # expiration it equal to zero
            except:
                Task.objects.filter(pk=task_id).update(
                    remaining_estimate=0)
        f.save()
