from django.contrib import admin
from .models import CategoriesOfReceipt, CategoriesOfSpending, FinansyBalance, Receipt, Spending


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
    list_display = ('com', 'category', 'date', 'type', 'deal', 'sum')
    search_fields = ['com', 'category', 'date', 'type', 'deal', 'sum']
    autocomplete_fields = ['deal', 'category']
    list_filter = ('category', 'type', 'deal')
    date_hierarchy = 'date'
    list_select_related = ('category',)
    # list_editable = ['sum', 'category']
    # list_display_links = ['com', 'category']

@admin.register(Spending)
class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('com', 'user_do', 'category', 'date', 'type', 'deal', 'sum')
    search_fields = ['com', 'user_do', 'category', 'date', 'type', 'deal', 'sum']
    autocomplete_fields = ['deal', 'category']
    list_filter = ('category', 'type', 'deal')
    date_hierarchy = 'date'
