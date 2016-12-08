from django.shortcuts import render
from jirello.models import User, Task, Sprint, ProjectModel
from jirello.forms import RegistrationForm, AuthenticationForm, ProjectForm
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login


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
    return render(request,
                  'jirello/register.html',
                  {'register_form': register_form})


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
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse(
                "Your username and password didn't match. Please try again.")
    else:
        return render(request, 'jirello/login.html', {'auth_form': auth_form})


@login_required(login_url='/jirello/login/')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/jirello/')


def main(request):
    task_list = Task.objects.all()
    sprint_list = Sprint.objects.all()
    context_dict = {
        'task_list': task_list,
        "sprint_list": sprint_list}
    return render(request, 'jirello/main_page.html', context_dict)


def password_change(request):
    pass


@login_required(login_url='/jirello/login/')
def projects(request):
    form = ProjectForm()
    # import pdb; pdb.set_trace()
    if ProjectModel.objects.filter(users__id=request.user.id).exists():
        print('ALL IN')
        projects_list = ProjectModel.objects.filter(users__id=request.user.id)
    else:
        print('FAIL')
        projects_list = 'sory you are have not any projects'
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid:
            form.save()

    context_dict = {'form' : form, 'projects_list' : projects_list}
    return render(request, 'jirello/project_page.html', context_dict)
