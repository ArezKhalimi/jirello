from django import forms
from jirello.models.user_model import User
from jirello.models.project_model import ProjectModel
from jirello.models.sprint_model import Sprint
from jirello.models.task_model import Task
from jirello.models.worklog_model import Worklog
from jirello.models.comment_model import Comment
from jirello.models.task_model import STATUSES, STORYPOINTS, KIND


class RegistrationForm(forms.ModelForm):
    # Form for registering a new account.
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }
        ),
        error_messages={'required': 'Please enter your name'}
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'id': "inputEmail",
            }
        ),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }
        ),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password',
            }
        ),
        label="Password (again)",
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'picture',
        ]

    def clean(self):
        # Verifies that the values entered into the password fields match
        # cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data \
                and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1']\
                    != self.cleaned_data['password2']:
                raise forms.ValidationError(
                    "Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()


class AuthenticationForm(forms.Form):
    # Login form
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Password',
                   }
        ),
    )

    class Meta:
        fields = [
            'username',
            'password',
        ]


class ProjectForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Project Title',
            }
        ),
    )
    description = forms.CharField(
        max_length=206,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Description',
                'rows': '4',
            }
        ),
    )
    users = forms.ModelMultipleChoiceField(
        # exclude AnonymousUser (special user for django-guardian)
        queryset=User.objects.all().exclude(pk=1),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = ProjectModel
        fields = [
            'title',
            'description',
            'users',
        ]


class SprintForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Title of sprint',
            }
        ),
    )

    date_start = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'datepicker',
                'placeholder': 'Sprint start date',
            }
        ),
        input_formats=['%d/%m/%Y']
    )

    date_end = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'datepicker-1',
                'placeholder': 'Sprint end date',
            }
        ),
        input_formats=['%d/%m/%Y']
    )

    is_active = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Sprint
        fields = [
            'title',
            'date_start',
            'date_end',
            'is_active',
        ]

# placeholder and help_text to template


class TaskForm(forms.ModelForm):

    def __init__(self, projectmodel_id, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.project = kwargs.pop('project', None)
        if self.project:
            self.project = ProjectModel.objects.get(id=self.project)
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields["worker"].queryset = User.objects.filter(
            projects__id=projectmodel_id).prefetch_related('projects')
        self.fields["worker"].help_text = 'Use CTRL for multiple choices'
        self.fields["sprints"].queryset = Sprint.objects.filter(
            project_id=projectmodel_id).order_by('date_end')
        self.fields["sprints"].help_text = 'Use CTRL for multiple choices'
        self.fields["parent"].queryset = Task.objects.filter(
            project_id=projectmodel_id)
        self.fields["worker"].widget.attrs = {'class': 'form-control', }
        self.fields["sprints"].widget.attrs = {'class': 'form-control', }
        self.fields["parent"].widget.attrs = {'class': 'form-control', }

    status = forms.ChoiceField(choices=STATUSES)

    title = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Title of task',
            }
        ),
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Description of task',
                'rows': '4',
            }
        ),
    )
    original_estimate = forms.IntegerField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': '!!!!!!!!INSTRUCTIONS!!!!!!',
                   }
        )
    )
    storypoints = forms.ChoiceField(
        choices=STORYPOINTS,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    kind = forms.ChoiceField(
        choices=KIND,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    status = forms.ChoiceField(
        choices=STATUSES,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
    )

    def save(self, *args, **kwargs):
        task = super(TaskForm, self).save(commit=False)
        if self.user:
            task.owner = self.user
        if self.project:
            task.project = self.project
        if task.remaining_estimate is None \
                or task.original_estimate < task.remaining_estimate:
            task.remaining_estimate = task.original_estimate
        task.save()
        self.save_m2m()

    class Meta:
        model = Task
        exclude = ['remaining_estimate', ]
        fields = [
            'title',
            'kind',
            'parent',
            'description',
            'status',
            'sprints',
            'original_estimate',
            'storypoints',
            'worker',
        ]


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        max_length=400,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '6',
            }
        ),
    )

    class Meta:
        model = Comment
        fields = [
            'comment',
        ]


class WorklogForm(forms.ModelForm):
    time_spend = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    time_representation = forms.CharField(max_length=10)
    comment = forms.CharField(
        max_length=400,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '6',
            }
        ),
    )

    class Meta:
        model = Worklog
        fields = [
            'comment',
            'time_representation',
            'time_spend',
        ]

    def save(self, *args, **kwargs):
        value = self.cleaned_data.pop('time_representation')
        splitted_value = value.split(' ')
        real_time = 0
        for item in splitted_value:
            if item[-1] in ['H', 'h'] and item[:-1].isdigit():
                real_time += 3600 * int(item[:-1])
            elif item[-1] in ['M', 'm'] and item[:-1].isdigit():
                real_time += 60 * int(item[:-1])
            elif item.isdigit():
                real_time += int(item)
            else:
                # raise form.ValidationError('wrong input')
                real_time = 0
        self.cleaned_data['time_spend'] = real_time
        return super(WorklogForm, self).save(*args, **kwargs)
