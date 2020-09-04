from django.contrib import admin
from .models import *


@admin.register(JobCategories)
class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


@admin.register(Performers)
class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('fio_min', 'all_sum', 'all_sum_already', 'all_debt')
    search_fields = ['name', 'surname', 'patronymic', ]
    ordering = ('name',)

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['osm_data'] = Affairs.objects.get(pk=object_id)
    #     return super(UserAccessAdmin, self).change_view(request, object_id,
    #                                                     form_url, extra_context=extra_context)
