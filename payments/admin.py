from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'transaction_id', 'amount', 'method', 'is_successful', 'timestamp')
    list_filter = ('is_successful', 'method', 'timestamp')
    search_fields = ('order_id', 'transaction_id')
