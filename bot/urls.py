from django.urls import path
from . import views

urlpatterns = [
    path('/promokods', views.promokods_all, name='promokodes_all'),
    path('/promokods/add', views.promo_add, name='promo_add'),
    path('/promokods/edit/<promo_id>', views.promo_edit, name='promo_edit'),
    ]
