from django.shortcuts import render, redirect
from .forms import RegForm, LoginForm, ChangePassForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


def index(request):
    print(request.user.is_authenticated)
    return render(request, 'main/index.html', {'auth': request.user.is_authenticated})


def login_acc(request):
    form = LoginForm()
    err = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return redirect('main_page')
            else:
                err = 'incorrect'

    return render(request, 'main/login.html', {'form': form, 'error': err})


def reg(request):
    form = RegForm()

    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'main/complete.html', {'name': new_user.username})
    return render(request, 'main/reg.html', {'form': form})


def profile(request):
    current_user = request.user
    if request.method == 'POST':
        if 'change' in request.POST:
            return redirect('change_pswrd')
        elif 'logout' in request.POST:
            logout(request)
            return redirect('main_page')
    return render(request, 'main/profile.html', {'user': current_user})


def complete(request):
    return render(request, 'main/complete.html')


def change_pswrd(request):
    err = ''
    form = ChangePassForm()
    current_user = request.user
    if request.method == 'POST':
        form = ChangePassForm(request.POST)
        if 'change' in request.POST and form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=current_user.username, password=data['old_pass'])
            if user is not None:
                current_user.set_password(data['new_pass'])
                current_user.save()
                logout(request)
                return redirect('login')
            else:
                err = 'Incorrect password!'
        elif 'to_main' in request.POST:
            return redirect('main_page')
        else:
            err = 'Incorrect input!'
    return render(request, 'main/change.html', {'form': form, 'error': err})
