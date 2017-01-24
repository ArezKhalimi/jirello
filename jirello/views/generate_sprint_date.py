from datetime import timedelta


def generate_sprint_date(sprint):
    date_list = []
    for n in range(int((sprint.date_end - sprint.date_start).days) + 1):
        date_list.append(sprint.date_start + timedelta(n))
    return date_list
