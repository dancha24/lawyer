from django.urls import path
from . import views

urlpatterns = [

    # Дела
    # path('', views.index, name='control_overview'),
    path('all', views.affairs_all, name='affairs_all'),
    path('add', views.affairs_add, name='affairs_add'),
    path('<affair_id>/', views.affairs_info, name='affairs_info'),
    path('<affair_id>/change', views.affairs_change, name='affairs_change'),
    # path('change/<affair_id>', views.affairs_change, name='affairs_change'),

    # Доп.дела
    path('extra/all', views.extra_affairs_all, name='extra_affairs_all'),
    path('extra/add', views.extra_affairs_add, name='extra_affairs_add'),
    path('extra/<extra_affairs_id>/', views.extra_affairs_info, name='extra_affairs_info'),
]
