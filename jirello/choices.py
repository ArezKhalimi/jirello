from .enumeration import Enumeration


KIND = Enumeration([
    (u'E', 'EPIC', u'Epic'),
    (u'S', 'STORY', u'Story'),
    (u'T', 'TASK', u'Task'),
    (u'B', 'BUG', u'Bug'),
    (u't', 'SUBTASK', u'SubTask'),
    (u'b', 'STORYBUG', u'StoryBug'),
])

STATUSES = Enumeration([
    (u'O', 'OPEN', u'Open'),
    (u'R', 'DEVELOP', u'Ready to develop'),
    (u'I', 'PROGRESS', u'In progress'),
    (u'C', 'REVIEW', u'Code Review'),
    (u'V', 'VERIFICATION', u'Verification'),
    (u'D', 'DONE', u'Done'),
])

STORYPOINTS = Enumeration([
    (1, 'ONE', '1'),
    (2, 'TWO', '2'),
    (3, 'THREE', '3'),
    (4, 'FIVE', '5'),
    (5, 'EIGHT', '8'),
    (6, 'THIRTEEN', '13'),
    (7, 'TWENTY-ONE', '21'),
])
