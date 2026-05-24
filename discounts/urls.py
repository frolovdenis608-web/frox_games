from django.urls import path
from .views import apply_promocode, promocode_create, promocode_delete

app_name = 'discounts'

urlpatterns = [
    path('apply/', apply_promocode, name='apply_promocode'),
    path('management/create/', promocode_create, name='promocode_create'),
    path('management/delete/<int:id>/', promocode_delete, name='promocode_delete'),
]