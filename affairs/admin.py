from django.contrib import admin
from .models import Affairs
from .forms import AffairsForm


@admin.register(Affairs)
class UserAccessAdmin(admin.ModelAdmin):
    change_list_template = 'admin/affairs_list.html'
    change_form_template = 'admin/affairs_view.html'
    add_form = AffairsForm
    form = AffairsForm
    list_display = ('name', 'customers', 'performer', 'jobcategories')
    list_filter = ('deal_status', 'prise_status', 'customers', 'performer', 'jobcategories')
    search_fields = ['name', 'customers', 'performer', 'jobcategories']
    autocomplete_fields = ['customers', 'performer', 'jobcategories']
    ordering = ('date_in',)
    date_hierarchy = 'date_in'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['deals_in_count'] = Affairs.deals_in_count()
        extra_context['deals_in_prise_sum'] = Affairs.deals_in_prise_sum()
        extra_context['deals_in_no_prise_count'] = Affairs.deals_in_no_prise_count()
        extra_context['deals_in_no_prise_sum'] = Affairs.deals_in_no_prise_sum()
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['osm_data'] = Affairs.objects.get(pk=object_id)
        return super(UserAccessAdmin, self).change_view(request, object_id,
                                                        form_url, extra_context=extra_context)
