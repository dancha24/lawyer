from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Performers, PerformersDoc
from finansy.models import Spending


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
