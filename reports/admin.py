from django.contrib import admin
from .models import FinsnsyRep


@admin.register(FinsnsyRep)
class UserAccessAdmin(admin.ModelAdmin):
    change_list_template = 'admin/FinRep.html'
    # change_form_template = 'admin/affairs_view.html'
