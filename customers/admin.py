from django.contrib import admin
from .models import *
from affairs.models import Affairs


class PerformersInline(admin.StackedInline):
    model = Affairs
    extra = 0
    # fk_name = 'customers'
    show_change_link = True
    # readonly_fields = ('name',)
    # list_display = ('name',)
    # fields = ('name',)
    exclude = (
        'name', 'prisealready', 'priseperformeralready', 'deal_status', 'prise_status',
        'performer', 'jobcategories', 'prise', 'date_in', 'date_out', 'priseperformer', 'deal')


@admin.register(WhereInfo)
class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


@admin.register(Customers)
class UserAccessAdmin(admin.ModelAdmin):
    readonly_fields = ('all_debt',)
    list_display = ('fio_min', 'all_sum', 'all_sum_already', 'all_debt')
    search_fields = ['name', 'surname', 'patronymic', ]
    # list_filter = ('fio_min',)
    inlines = (PerformersInline,)

    # def get_queryset(self, request):
    #     qs = super(UserAccessAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(author=request.user)

# class CustomUserAdmin(Customers):
#     model = Customers
    # list_display = ('fio_min',)
    # list_filter = ('fio_min',)
    # fieldsets = (
    #     ('Основное', {'fields': ('email', 'password', 'namepark', 'tel', 'city')}),
    #     ('Права', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups')}),
    # )
    # add_fieldsets = (
    #     ('Основное', {
    #         'classes': ('wide',),
    #         'fields': ('email', 'namepark', 'tel', 'city', 'password1', 'password2')}
    #      ), ('Права', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups')})
    # )
    # search_fields = ('fio_min',)
    # ordering = ('fio_min',)


# admin.site.register(CustomUserAdmin)
