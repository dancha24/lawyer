from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from .forms import *
from django.views.generic import FormView, CreateView, ListView

urlpatterns = [
    path('finansy_today/all', views.finansy_today_all, name='finansy_today_all'),
    path('finansy_today/<y>/<m>/<d>', views.finansy_today_date, name='finansy_today_date'),
]
