from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth import login as auth_login

from jirello.forms import AuthenticationForm


def login(request):
    auth_form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth_authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/jirello/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse(
                "Your username and password didn't match. Please try again."
            )
    else:
        return render(request, 'jirello/login.html', {'auth_form': auth_form})
