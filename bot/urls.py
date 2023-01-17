from django.urls import path
from bot import views

urlpatterns = [
    path('promokods', views.promokods_all, name='promokodes_all'),
    path('promokods/add', views.promo_add, name='promo_add'),
    path('promokods/edit/<promo_id>', views.promo_edit, name='promo_edit'),
    path('botset/', views.botset, name='botset'),
    path('botset/edit/<set_id>', views.set_edit, name='set_edit'),
    path('gendokaren', views.gendokaren, name='gendokaren'),
    path('gensprav', views.gensprav, name='gensprav'),
    path('charts', views.charts, name='charts'),
    # path('botset/reload', views.botreload, name='botreload'),
    ]
