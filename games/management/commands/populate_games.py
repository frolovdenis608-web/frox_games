from django.core.management.base import BaseCommand
from django.utils.text import slugify
from games.models import Game, Genre
from datetime import date
import uuid


class Command(BaseCommand):
    help = 'Заповнює базу даних списком ігор з кількома жанрами та віковими рейтингами'

    def handle(self, *args, **kwargs):
        games_data = [
            {"name": "Elden Ring", "price": 3999, "genres": ["RPG", "Action", "Dark Fantasy"], "age_rating": "16+",
             "img": "Elden_Ring_-_cover.jpg"},
            {"name": "Cyberpunk 2077", "price": 2499, "genres": ["Action", "RPG", "Sci-Fi", "Open World"],
             "age_rating": "18+", "img": "Обложка_компьютерной_игры_Cyberpunk_2077.jpg"},
            {"name": "Starcraft II", "price": 999, "genres": ["Strategy", "Sci-Fi", "RTS"], "age_rating": "16+",
             "img": "SC2_Heart_of_the_Swarm_cover.jpg"},
            {"name": "The Witcher 3", "price": 1500, "genres": ["RPG", "Action", "Fantasy", "Open World"],
             "age_rating": "18+", "img": "20201101185506!The_Witcher_3-_Wild_Hunt_Cover.jpg"},
            {"name": "Rust", "price": 779, "genres": ["Survival", "Action", "Multiplayer"], "age_rating": "18+",
             "img": "art_image-rust-01c6b8a4.original.jpg"},
            {"name": "GTA 5", "price": 1349, "genres": ["Action", "Shooter", "Open World", "Multiplayer"],
             "age_rating": "18+", "img": "GTAV_Official_Cover_Art.jpg"},
            {"name": "Sid Meier's Civilization VI", "price": 525, "genres": ["Strategy", "Simulation", "Historical"],
             "age_rating": "12+", "img": "Civilization_VI_cover_art.jpg"},
            {"name": "Hearts of Iron IV", "price": 1349, "genres": ["Strategy", "Simulation", "Historical"],
             "age_rating": "12+", "img": "Hearts_of_Iron_IV_-_cover.png"},
            {"name": "Path of Exile 2", "price": 600, "genres": ["RPG", "Action", "Hack & Slash", "Multiplayer"],
             "age_rating": "18+", "img": "Path_of_Exile_2.jpg"},
            {"name": "The Elder Scrolls V: Skyrim Special Edition", "price": 649,
             "genres": ["RPG", "Fantasy", "Open World"], "age_rating": "18+", "img": "images.JFIF"},
            {"name": "Watch_Dogs™", "price": 429, "genres": ["Action", "Stealth", "Open World"], "age_rating": "18+",
             "img": "Watch_Dogs.JFIF"},
            {"name": "Watch_Dogs® 2", "price": 915, "genres": ["Action", "Stealth", "Open World", "Multiplayer"],
             "age_rating": "18+", "img": "Watch_Dogs_2_cover.jpg"},
            {"name": "Sleeping Dogs: Definitive Edition", "price": 379, "genres": ["Action", "Fighting", "Open World"],
             "age_rating": "18+", "img": "Sleeping Dogs Definitive Edition.WEBP"},
            {"name": "Outlast", "price": 325, "genres": ["Horror", "Survival", "Indie"], "age_rating": "18+",
             "img": "Outlast.JFIF"},
            {"name": "Resident Evil Requiem", "price": 1999, "genres": ["Horror", "Action", "Survival"],
             "age_rating": "18+", "img": "resident-evil-requiem-g8jiq.jpg"},
            {"name": "Battlefield™ 6", "price": 1699, "genres": ["Action", "Shooter", "Multiplayer", "FPS"],
             "age_rating": "16+", "img": "Battlefield_6_cover_art.jpg"},
            {"name": "Amnesia: The Bunker", "price": 515, "genres": ["Horror", "Survival", "Puzzle"],
             "age_rating": "18+", "img": "Amnesia_The_Bunker_cover.webp"},
            {"name": "Conan Exiles Enhanced", "price": 479, "genres": ["Survival", "RPG", "Open World"],
             "age_rating": "18+", "img": "Conan Exiles Enhanced.webp"},
            {"name": "Subnautica 2", "price": 899, "genres": ["Survival", "Sci-Fi", "Exploration", "Open World"],
             "age_rating": "12+", "img": "Subnautica 2.jpg"},
            {"name": "Forza Horizon 6", "price": 2299, "genres": ["Racing", "Simulation", "Open World", "Sports"],
             "age_rating": "0+", "img": "Forza Horizon 6.png"},
            {"name": "Assetto Corsa Competizione", "price": 999, "genres": ["Racing", "Simulation", "Sports"],
             "age_rating": "0+", "img": "Assetto Corsa Competizione.jpg"},
            {"name": "Need for Speed™ Unbound", "price": 1699, "genres": ["Racing", "Action", "Arcade"],
             "age_rating": "12+", "img": "Need for Speed™ Unbound.png"},
            {"name": "Outlast 2", "price": 415, "genres": ["Horror", "Survival", "Gore"], "age_rating": "18+",
             "img": "Outlast 2.png"},
            {"name": "Dead by Daylight", "price": 425, "genres": ["Horror", "Survival", "Multiplayer", "Action"],
             "age_rating": "18+", "img": "Dead by Daylight.jpg"},
            {"name": "Call of Duty®: Modern Warfare®", "price": 1349,
             "genres": ["Action", "Shooter", "FPS", "Multiplayer"], "age_rating": "18+",
             "img": "Call of Duty Modern Warfare.jpg"},
            {"name": "Baldur's Gate 3", "price": 899, "genres": ["RPG", "Fantasy", "Strategy", "Story Rich"],
             "age_rating": "18+", "img": "Baldur's Gate 3.png"},
            {"name": "Diablo® IV", "price": 1966, "genres": ["RPG", "Action", "Dark Fantasy", "Hack & Slash"],
             "age_rating": "18+", "img": "Diablo IV.jfif"},
            {"name": "Kingdom Come: Deliverance II", "price": 2132,
             "genres": ["RPG", "Historical", "Action", "Open World"], "age_rating": "18+", "img": "1.jpg"},
            {"name": "Kingdom Come: Deliverance", "price": 1000,
             "genres": ["RPG", "Historical", "Action", "Open World"], "age_rating": "18+", "img": "2.jpg"},
            {"name": "The Long Dark", "price": 399, "genres": ["Survival", "Simulation", "Atmospheric"],
             "age_rating": "16+", "img": "The Long Dark.WEBP"},
            {"name": "Don't Starve Together", "price": 229, "genres": ["Survival", "Multiplayer", "Indie", "2D"],
             "age_rating": "12+", "img": "Don't Starve Together.jpg"},
            {"name": "Raft", "price": 499, "genres": ["Survival", "Multiplayer", "Indie", "Open World"],
             "age_rating": "12+", "img": "Raft.jpg"},
            {"name": "Project Zomboid", "price": 415, "genres": ["Survival", "RPG", "Horror", "Simulation"],
             "age_rating": "18+", "img": "Project Zomboid.jpg"},
            {"name": "Sons Of The Forest", "price": 600, "genres": ["Survival", "Horror", "Action", "Multiplayer"],
             "age_rating": "18+", "img": "Sons Of The Forest.jpg"},
            {"name": "ARK: Survival Ascended", "price": 1645,
             "genres": ["Survival", "Action", "Multiplayer", "Open World"], "age_rating": "16+",
             "img": "ARK Survival Ascended.jpg"},
            {"name": "Valheim", "price": 539, "genres": ["Survival", "RPG", "Multiplayer", "Open World"],
             "age_rating": "12+", "img": "Valheim.png"},
        ]

        added_count = 0

        for item in games_data:

            base_slug = slugify(item["name"])
            slug = base_slug
            if Game.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"

            if not Game.objects.filter(title=item["name"]).exists():

                genres_text = ", ".join(item["genres"])
                desc = f"Це детальний опис для гри {item['name']}. Справжній шедевр у жанрах: {genres_text}."

                game = Game.objects.create(
                    title=item["name"],
                    slug=slug,
                    description=desc,
                    price=item["price"],
                    age_rating=item["age_rating"],
                    release_date=date.today(),
                    developer="FroxGameS Partner",
                    cover_image=f"games_image/{item['img']}",
                    is_active=True
                )

                for genre_name in item["genres"]:

                    genre_obj, _ = Genre.objects.get_or_create(
                        name=genre_name,
                        defaults={'slug': slugify(genre_name)}
                    )
                    game.genres.add(genre_obj)

                self.stdout.write(self.style.SUCCESS(f'Гру "{game.title}" успішно додано!'))
                added_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'Гра "{item["name"]}" вже існує. Пропускаємо.'))

        self.stdout.write(self.style.SUCCESS(f'Завершено! Додано ігор: {added_count}'))