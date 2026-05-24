from django.urls import path
from .views import GameListView, GameDetailView, game_create, game_edit, genre_create, game_delete, genre_delete

app_name = 'games'

urlpatterns = [
    path('', GameListView.as_view(), name='game_list'),
    path('game/<slug:slug>/', GameDetailView.as_view(), name='game_detail'),
    path('management/game/add/', game_create, name='game_create'),
    path('management/game/edit/<int:id>/', game_edit, name='game_edit'),
    path('management/genre/add/', genre_create, name='genre_create'),
    path('management/game/delete/<int:id>/', game_delete, name='game_delete'),
    path('management/genre/delete/<int:id>/', genre_delete, name='genre_delete'),
]