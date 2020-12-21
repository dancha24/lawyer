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
        'customers', 'jobcategories', 'prise', 'date_in', 'date_out', 'priseperformer', 'deal')


@admin.register(JobCategories)
class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


@admin.register(Performers)
class UserAccessAdmin(admin.ModelAdmin):
    change_list_template = 'admin/performers_list.html'
    # change_form_template = 'admin/performers_view.html'
    list_display = ('fio_min', 'all_sum', 'all_sum_already', 'all_debt')
    search_fields = ['name', 'surname', 'patronymic', ]
    inlines = (PerformersInline,)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['all_sum_all_performers'] = Performers.all_sum_all_performers()
        extra_context['all_sum_already_all_performers'] = Performers.all_sum_already_all_performers()
        extra_context['all_debt_all_performers'] = Performers.all_debt_all_performers()
        # extra_context['deals_in_no_prise_count'] = Affairs.deals_in_no_prise_count()
        # extra_context['deals_in_no_prise_sum'] = Affairs.deals_in_no_prise_sum()
        return super().changelist_view(request, extra_context=extra_context)

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['osm_data'] = Affairs.objects.get(pk=object_id)
    #     return super(UserAccessAdmin, self).change_view(request, object_id,
    #                                                     form_url, extra_context=extra_context)

# @admin.register(Performers)
# class UserAccessAdmin(admin.ModelAdmin):
#     list_display = ('fio_min', 'all_sum', 'all_sum_already', 'all_debt')
#     search_fields = ['name', 'surname', 'patronymic', ]
#     ordering = ('name',)

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['osm_data'] = Affairs.objects.get(pk=object_id)
    #     return super(UserAccessAdmin, self).change_view(request, object_id,
    #                                                     form_url, extra_context=extra_context)


@admin.register(PerformersDoc)
class UserAccessAdmin(admin.ModelAdmin):
    # list_display = ('fio_min', 'all_sum', 'all_sum_already', 'all_debt')
    # search_fields = ['name', 'surname', 'patronymic', ]
    ordering = ('name',)

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['osm_data'] = Affairs.objects.get(pk=object_id)
    #     return super(UserAccessAdmin, self).change_view(request, object_id,
    #                                                     form_url, extra_context=extra_context)
