from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import logout


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('overview')
    else:
        return redirect('login')


def overview(request):
    context = {
        'menu': 'overview',
        'submenu': 'overview',
        'titlepage': 'Обзор',
    }

    return render(request, 'index/ov.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('control_overview')
    context = {
        'titlepage': 'Вход',
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Правильный пароль и пользователь "активен"
            auth.login(request, user)
            # Перенаправление на "правильную" страницу
            return redirect('overview')
        else:
            # Отображение страницы с ошибкой
            return HttpResponseRedirect("/")
    return render(request, 'index/login.html', context)


# Выход
def out(request):
    logout(request)
    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
