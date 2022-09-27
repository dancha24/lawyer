from django.urls import path
from . import views
from .views import PromoSearchByNameView

urlpatterns = [
    path('promo/search/name/<search>', PromoSearchByNameView.as_view(), name='api_search_promo'),
]
