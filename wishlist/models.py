# wishlist/models.py
from django.db import models
from django.conf import settings
from games.models import Game

class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    games = models.ManyToManyField(Game, related_name='wished_by', blank=True, verbose_name="Ігри у списку бажаного")

    class Meta:
        verbose_name = "Список бажаного"
        verbose_name_plural = "Списки бажаного"

    def __str__(self):
        return f"Список бажаного: {self.user.username}"