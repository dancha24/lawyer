from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Performers, PerformersDoc
from finansy.models import Spending
from . import forms
from django.shortcuts import redirect


# Добавление исполнителя
@permission_required('performers.add_performers', raise_exception=True)
def performers_add(request):
    if request.method == "POST":
        form = forms.PerformersAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if 'add' in request.POST and request.POST['add']:
                return redirect('performers_add')
            else:
                return redirect('performers_info', performers_id=form.save().id)
    else:
        form = forms.PerformersAddForm()
    context = {
        'menu': 'performers',
        'submenu': 'performers_add',
        'form': form,
        'titlepage': 'Добавление исполнителя',
    }

    return render(request, 'performers/performers_add.html', context)


# Список всех Исаолнителей
@permission_required('performers.view_performers', raise_exception=True)  # Проверка прав
def performers_all(request):
    performers = Performers.objects.all()
    context = {
        'for_table': performers,
        'menu': 'performers',
        'submenu': 'performers_all',
        'titlepage': 'Список Исполнителей',
    }

    return render(request, 'performers/performers_all.html', context)


# Информация об Исполнителе
@permission_required('performers.view_performers', raise_exception=True)  # Проверка прав
def performers_info(request, performers_id):
    performers = Performers.objects.get(pk=performers_id)
    spending = Spending.objects.filter(performers_id=performers_id)
    context = {
        'info': performers,
        'spending': spending,
        # 'extra_affairs': extra_affairs,
        # 'performers': performers_with_prise,
        'menu': 'performers',
        'submenu': 'performers_all',
        'titlepage': 'Информация о деле ' + str(performers),
    }

    return render(request, 'performers/performers_info.html', context)
