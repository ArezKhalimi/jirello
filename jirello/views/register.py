from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth import login as auth_login

from jirello.forms import RegistrationForm


def register(request):
    register_form = RegistrationForm()
    if request.method == 'POST':
        register_form = RegistrationForm(
            data=request.POST,
            files=request.FILES)
        if register_form.is_valid():
            register_form.save()
            new_user = auth_authenticate(
                username=register_form.cleaned_data['username'],
                password=register_form.cleaned_data['password1'],
            )
            auth_login(request, new_user)
            return HttpResponseRedirect("/jirello/")
    return render(
        request,
        'jirello/register.html',
        {'register_form': register_form}
    )
