from django.db import models
from django.conf import settings
from games.models import Game


class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Очікує оплати'),
        ('PAID', 'Оплачено'),
        ('COMPLETED', 'Виконано (Ключі надіслані)'),
        ('CANCELED', 'Скасовано'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Загальна сума")

    def __str__(self):
        return f"Замовлення #{self.id} від {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    license_key = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ключ активації")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.game.title} (x{self.quantity})"