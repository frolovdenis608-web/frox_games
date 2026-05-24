# payments/urls.py
from django.urls import path
from .views import process_payment, payment_success

app_name = 'payments'

urlpatterns = [
    path('process/<int:order_id>/', process_payment, name='process_payment'),
    path('success/', payment_success, name='payment_success'),
]