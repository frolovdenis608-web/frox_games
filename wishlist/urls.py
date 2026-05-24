from django.urls import path
from .views import wishlist_detail, toggle_wishlist

app_name = 'wishlist'

urlpatterns = [
    path('', wishlist_detail, name='wishlist_detail'),
    path('toggle/<int:game_id>/', toggle_wishlist, name='toggle_wishlist'),
]