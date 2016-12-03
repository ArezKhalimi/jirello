from django import forms
from accounts.models import User


class RegistrationForm(forms.ModelForm):
    # Form for registering a new account.
    username = forms.CharField(
        error_messages={'required': 'Please enter your name'})
    email = forms.EmailField(widget=forms.widget.TextInput, label="Email")
    password1 = forms.CharField(widget=forms.widget.PasswordInput,
                                label="Password")
    password2 = forms.CharField(widget=forms.widget.PasswordInput,
                                label="Password (again)")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

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
    username = forms.CharField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ['username', 'password']
