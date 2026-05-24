from django.contrib import admin
from .models import Game, Genre

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'release_date', 'is_active')
    list_filter = ('is_active', 'genres')
    search_fields = ('title', 'developer')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
