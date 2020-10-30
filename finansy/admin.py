from django.contrib import admin
from .models import CategoriesOfReceipt, CategoriesOfSpending, FinansyBalance, Receipt, Spending
from .forms import DateForm



@admin.register(CategoriesOfReceipt)
class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


@admin.register(CategoriesOfSpending)
class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


@admin.register(FinansyBalance)
class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('type', 'sum',)
    ordering = ['id']


@admin.register(Receipt)
class UserAccessAdmin(admin.ModelAdmin):
    change_list_template = 'admin/receipt.html'
    add_forms = DateForm
    forms = DateForm
    list_display = ('com', 'category', 'date', 'type', 'deal', 'sum')
    search_fields = ['com', 'category', 'date', 'type', 'deal', 'sum']
    autocomplete_fields = ['deal', 'category']
    list_filter = ('category', 'type', 'deal')
    date_hierarchy = 'date'
    list_select_related = ('category',)
    # list_editable = ['sum', 'category']
    # list_display_links = ['com', 'category']
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['filter'] = Receipt.filter(request)
        extra_context['receipt_in_count'] = Receipt.receipt_in_count()
        extra_context['receipt_in_prise_sum'] = Receipt.receipt_in_prise_sum()
        extra_context['receipt_in_count_mount'] = Receipt.receipt_in_count_mount()
        extra_context['receipt_in_prise_sum_mount'] = Receipt.receipt_in_prise_sum_mount()
        extra_context['receipt_in_count_all_time'] = Receipt.receipt_in_count_all_time()
        extra_context['receipt_in_prise_sum_all_time'] = Receipt.receipt_in_prise_sum_all_time()
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Spending)
class UserAccessAdmin(admin.ModelAdmin):
    change_list_template = 'admin/spending.html'
    add_forms = DateForm
    forms = DateForm
    list_display = ('com', 'user_do', 'category', 'date', 'type', 'deal', 'sum')
    search_fields = ['com', 'user_do', 'category', 'date', 'type', 'deal', 'sum']
    autocomplete_fields = ['deal', 'category']
    list_filter = ('category', 'type', 'deal')
    date_hierarchy = 'date'
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['filter'] = Spending.filter(request)
        extra_context['spending_in_count'] = Spending.spending_in_count()
        extra_context['spending_in_prise_sum'] = Spending.spending_in_prise_sum()
        extra_context['spending_in_count_mount'] = Spending.spending_in_count_mount()
        extra_context['spending_in_prise_sum_mount'] = Spending.spending_in_prise_sum_mount()
        extra_context['spending_in_count_all_time'] = Spending.spending_in_count_all_time()
        extra_context['spending_in_prise_sum_all_time'] = Spending.spending_in_prise_sum_all_time()
        return super().changelist_view(request, extra_context=extra_context)
