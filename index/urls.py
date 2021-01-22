from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index_general'),
    path('overview/', views.overview, name='overview'),
    path('login/', views.login, name='login'),
    path('logout/', views.out, name='log_out'),
]