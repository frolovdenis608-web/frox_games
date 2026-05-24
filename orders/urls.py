# orders/urls.py
from django.urls import path
from .views import cart_detail, cart_add, cart_remove, order_create

app_name = 'orders'

urlpatterns = [
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:game_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:game_id>/', cart_remove, name='cart_remove'),
    path('checkout/', order_create, name='order_create'),
]