from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from .forms import *
from django.views.generic import FormView, CreateView, ListView

urlpatterns = [
    path('finansy_today/all', views.finansy_today_all, name='finansy_today_all'),
    path('finansy_period', views.finansy_today_period, name='finansy_today_period'),
    path('finansy_period/<y>/<m>/<d>/<y2>/<m2>/<d2>', views.finansy_today_period, name='finansy_today_period_'),
    path('finansy_today/<y>/<m>/<d>', views.finansy_today_date, name='finansy_today_date'),
    path('dealreports/all', views.dealreports, name='dealreports'),
    path('settings', views.settings, name='settings'),
    #
    path('receipt/add', views.receipt_add, name='receipt_add'),
    path('receipt/<receipt_id>', views.receipt_info, name='receipt_info'),
    path('receipt/<receipt_id>/del', views.receipt_del, name='receipt_del'),
    path('receipt/<receipt_id>/edit', views.receipt_edit, name='receipt_edit'),

    path('spending/add', views.spending_add, name='spending_add'),
    path('spending/all', views.spending_all, name='spending_all'),
    path('spending/<spending_id>', views.spending_info, name='spending_info'),
    path('spending/<spending_id>/del', views.spending_del, name='spending_del'),
    path('spending/<spending_id>/edit', views.spending_edit, name='spending_edit'),
]
