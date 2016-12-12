from django import forms
from jirello.models.user_model import User
from jirello.models.project_model import ProjectModel
from jirello.models.project_model import Sprint


class RegistrationForm(forms.ModelForm):
    # Form for registering a new account.
    username = forms.CharField(
        error_messages={'required': 'Please enter your name'})
    email = forms.EmailField(widget=forms.TextInput, label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="Password (again)")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'picture', ]

    def clean(self):
        # Verifies that the values entered into the password fields match
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
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
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['username', 'password']


class ProjectForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=100)
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = ProjectModel
        fields = ['title', 'description', 'users']


class SprintForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    date_start = forms.DateField(
        widget=forms.widgets.DateInput(format="%d/%m/%Y"))
    date_end = forms.DateField(
        widget=forms.widgets.DateInput(format="%d/%m/%Y"))
    is_active = forms.BooleanField()

    # def __init__(self, *args, **kwargs):
    #    self.request = kwargs.pop('request', None)
    #    return super(SprintForm, self).__init__(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     kwargs['commit'] = False
    #     obj = super(SprintForm, self).save(*args, **kwargs)
    #     if self.request:
    #         obj.owner = self.request.user
    #     obj.save()
    #     return obj

    class Meta:
        model = Sprint
        #exclude = ('owner', )
        fields = ('title', 'date_start', 'date_end', 'is_active')
