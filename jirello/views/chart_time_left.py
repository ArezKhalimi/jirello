from jirello.views.chart_time_spend import chart_time_spend


def chart_time_left(sprint, dates_kwarg, date):
    duration = \
        sprint.sprint_original_estimate - \
        chart_time_spend(sprint, dates_kwarg, date)
    if duration < 0:
        return 0
    return duration
