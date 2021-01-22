from django.urls import path
from . import views

urlpatterns = [

    # Исполнители
    # path('', views.index, name='control_overview'),
    path('all', views.performers_all, name='performers_all'),
    path('<performers_id>/', views.performers_info, name='performers_info'),

    # Доп.дела
    # path('extra/all', views.extra_affairs_all, name='extra_affairs_all'),
    # path('extra/<extra_affairs_id>/', views.extra_affairs_info, name='extra_affairs_info'),
]
