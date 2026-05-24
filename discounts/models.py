from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class PromoCode(models.Model):
    DISCOUNT_TYPES = (
        ('PERCENT', 'Відсоток (%)'),
        ('FIXED', 'Сума в гривнях (грн)'),
    )

    code = models.CharField(max_length=50, unique=True, verbose_name="Промокод")
    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPES,
        default='PERCENT',
        verbose_name="Тип знижки"
    )
    value = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Значення знижки"
    )
    valid_from = models.DateTimeField(default=timezone.now, verbose_name="Діє з")
    valid_to = models.DateTimeField(verbose_name="Діє до")
    active = models.BooleanField(default=True, verbose_name="Активний")

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоди"

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to

    def __str__(self):
        if self.discount_type == 'PERCENT':
            return f"{self.code} (-{self.value}%)"
        return f"{self.code} (-{self.value} грн)"