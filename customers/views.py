from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Customers, WhereInfo
from finansy.models import Spending
from . import forms
from django.shortcuts import redirect
from .defs import gen_dog_arenda, gen_sprav_kaspi_one, gen_sprav_kaspi_two, gen_sprav_bel
from django.contrib import messages


# Список всех клиентов
@permission_required('customers.view_customers', raise_exception=True)  # Проверка прав
def customers_all(request):
    if request.user.is_superuser:
        customers = Customers.objects.all()
    else:
        customers = Customers.objects.filter(byuser=request.user)
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
    if request.method == "POST" and 'doppolya' in request.POST:
        form = forms.CustomerDopPoleForm(request.POST, request.FILES, instance=customers)
        if form.is_valid():
            send = form.save(commit=False)
            send.save()
            return redirect('customers_info', customers_id=customers_id)
    else:
        form = forms.CustomerDopPoleForm(instance=customers)
    if request.method == "POST" and 'spravkaspione' in request.POST:
        if customers.cityfiktiv is None:
            messages.info(request, 'Не заполнен фиктивный город в дополнительных полях')
        else:
            if customers.adresfiktiv is None:
                messages.info(request, 'Не заполнен фиктивный адрес в дополнительных полях')
            else:
                return gen_sprav_kaspi_one(customers_id)
    if request.method == "POST" and 'dogadenda' in request.POST:
        if customers.cityfiktiv is None:
            messages.info(request, 'Не заполнен фиктивный город в дополнительных полях')
        else:
            if customers.adresfiktiv is None:
                messages.info(request, 'Не заполнен фиктивный адрес в дополнительных полях')
            else:
                return gen_dog_arenda(customers_id)
    if request.method == "POST" and 'spravkaspitwo' in request.POST:
        if customers.cityfiktiv is None:
            messages.info(request, 'Не заполнен фиктивный город в дополнительных полях')
        else:
            if customers.adresfiktiv is None:
                messages.info(request, 'Не заполнен фиктивный адрес в дополнительных полях')
            else:
                return gen_sprav_kaspi_two(customers_id)
    if request.method == "POST" and 'spravbel' in request.POST:
        if customers.cityfiktiv is None:
            messages.info(request, 'Не заполнен фиктивный город в дополнительных полях')
        else:
            if customers.adresfiktiv is None:
                messages.info(request, 'Не заполнен фиктивный адрес в дополнительных полях')
            else:
                return gen_sprav_bel(customers_id)
    context = {
        'info': customers,
        'form': form,
        'spending': spending,
        # 'extra_affairs': extra_affairs,
        # 'performers': performers_with_prise,
        'menu': 'customers',
        'submenu': 'customers_all',
        'titlepage': 'Информация о клиенте ' + str(customers),
    }

    return render(request, 'customers/customers_info.html', context)

# Добавление записи расхода
@permission_required('customers.add_customers', raise_exception=True)
def customers_add(request):
    if request.method == "POST":
        form = forms.CustomerAddForm(request.POST)
        if form.is_valid():
            form.save()
            customers = Customers.objects.get(pk=form.instance.id)
            customers.byuser = request.user
            customers.save()
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
    if request.method == "POST":
        form = forms.InfoAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('informations_all')
    else:
        form = forms.InfoAddForm()

    if request.method == "POST" and 'informations_del' in request.POST:
        uid = request.POST['id']
        informations_del(uid)

    context = {
        'for_table': where,
        'form': form,
        'menu': 'customers',
        'submenu': 'informations_all',
        'titlepage': 'Источники информации',
    }

    return render(request, 'customers/informations_all.html', context)

