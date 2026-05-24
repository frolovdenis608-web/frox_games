from django.db import models
from orders.models import Order

class Payment(models.Model):
    METHOD_CHOICES = (
        ('STRIPE', 'Stripe'),
        ('LIQPAY', 'LiqPay'),
        ('TEST', 'Тестова оплата'),
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ID транзакції")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сума")
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"Оплата до замовлення #{self.order.id} - {'Успішно' if self.is_successful else 'В процесі'}"