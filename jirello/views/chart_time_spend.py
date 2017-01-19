def chart_time_spend(sprint, dates_kwarg, date):
    time_spend = getattr(sprint, dates_kwarg[date])
    if not time_spend:
        return 0
    return time_spend
