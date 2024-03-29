from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Customers, WhereInfo
from finansy.models import Spending
from . import forms
from django.shortcuts import redirect


# Список всех клиентов
@permission_required('customers.view_customers', raise_exception=True)  # Проверка прав
def customers_all(request):
    customers = Customers.objects.all()
    context = {
        'for_table': customers,
        'menu': 'customers',
        'submenu': 'customers_all',
        'titlepage': 'Список Клиентов',
    }

    return render(request, 'customers/customers_all.html', context)


# Информация об Исполнителе
@permission_required('customers.view_customers', raise_exception=True)  # Проверка прав
def customers_info(request, customers_id):
    customers = Customers.objects.get(pk=customers_id)
    spending = Spending.objects.filter(performers_id=customers_id)
    context = {
        'info': customers,
        'spending': spending,
        # 'extra_affairs': extra_affairs,
        # 'performers': performers_with_prise,
        'menu': 'customers',
        'submenu': 'customers_all',
        'titlepage': 'Информация о клиенте ' + str(customers),
    }

    return render(request, 'customers/customers_info.html', context)

# Добавление записи расхода
@permission_required('cutomers.add_customers', raise_exception=True)
def customers_add(request):
    if request.method == "POST":
        form = forms.CustomerAddForm(request.POST)
        if form.is_valid():
            form.save()
            if 'add' in request.POST and request.POST['add']:
                return redirect('customers_add')
            else:
                return redirect('customers_all')
    else:
        form = forms.CustomerAddForm()
    context = {
        'menu': 'customers',
        'submenu': 'customers_all',
        'form': form,
        'titlepage': 'Добавление клиента',
    }

    return render(request, 'customers/customers_add.html', context)

@permission_required('customers.change_customers', raise_exception=True)
def customers_edit(request, customers_id):
    customers = Customers.objects.get(pk=customers_id)
    if request.method == "POST":
        form = forms.CustomersForm(request.POST, request.FILES, instance=customers)
        if form.is_valid():
            send = form.save(commit=False)
            # send.user = request.user
            send.save()
            if 'addp' in request.POST and request.POST['addp']:
                return redirect('customers_add')
            else:
                return redirect('customers_info', customers_id=form.save().id)
    else:
        form = forms.CustomersForm(instance=customers)
    context = {
        'titlepage': 'Редактирование клиента',
        'form': form,
    }
    return render(request, 'customers/customers_add.html', context)
# Удаление записи расхода
def informations_del(uid):
    for_del = WhereInfo.objects.get(id=uid)
    for_del.delete()
# Список всех источников информации

@permission_required('customers.view_informations', raise_exception=True)  # Проверка прав
def informations_all(request):
    where = WhereInfo.objects.all()
    context = {
        'for_table': where,
        'menu': 'customers',
        'submenu': 'informations_all',
        'titlepage': 'Источники информации',
    }
    if request.method == "POST" and 'informations_del' in request.POST:
        uid = request.POST['id']
        informations_del(uid)
        return render(request, 'customers/informations_all.html', context)

    return render(request, 'customers/informations_all.html', context)

