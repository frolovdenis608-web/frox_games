from django.core.management.base import BaseCommand
from games.models import Game, Genre


class Command(BaseCommand):
    help = 'Видаляє всі ігри та жанри з бази даних'

    def handle(self, *args, **kwargs):
        # Видаляємо всі ігри
        games_deleted, _ = Game.objects.all().delete()

        # Видаляємо всі жанри
        genres_deleted, _ = Genre.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(f'Успішно очищено! Видалено ігор: {games_deleted}, жанрів: {genres_deleted}.'))