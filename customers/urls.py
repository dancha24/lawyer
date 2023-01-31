from django.urls import path
from . import views

urlpatterns = [
    path('all', views.customers_all, name='customers_all'),
    path('<customers_id>/', views.customers_info, name='customers_info'),
    path('edit/<customers_id>/', views.customers_edit, name='customers_edit'),
    path('add', views.customers_add, name='customers_add'),
    path('infoall', views.informations_all, name='informations_all'),
    path('info/<informations_id>/del', views.informations_del, name='informations_del'),
    path('info/cashin', views.infocashin, name='infocashin'),
    #path('infoall/<whereinfo_id>/delete', views.informations_delete, name='informations_delete'),
]
