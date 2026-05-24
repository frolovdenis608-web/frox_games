from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва жанру")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Game(models.Model):
    AGE_RATINGS = (
        ('0+', '0+ (Для всіх)'),
        ('6+', '6+'),
        ('12+', '12+'),
        ('16+', '16+'),
        ('18+', '18+ (Дорослі)'),
    )

    title = models.CharField(max_length=255, verbose_name="Назва гри")
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    discount_percent = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Знижка (%)"
    )

    age_rating = models.CharField(
        max_length=5,
        choices=AGE_RATINGS,
        default='0+',
        verbose_name="Віковий рейтинг"
    )
    release_date = models.DateField(verbose_name="Дата виходу")
    developer = models.CharField(max_length=255, verbose_name="Розробник")
    genres = models.ManyToManyField(Genre, related_name='games', verbose_name="Жанри")
    cover_image = models.ImageField(upload_to='games/covers/', verbose_name="Обкладинка")
    is_active = models.BooleanField(default=True, verbose_name="Доступна для продажу")

    @property
    def get_discounted_price(self):
        if self.discount_percent > 0:
            discount_amount = (self.price * self.discount_percent) / 100
            return round(self.price - discount_amount, 2)
        return self.price

    def __str__(self):
        return self.title