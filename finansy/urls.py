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
]
