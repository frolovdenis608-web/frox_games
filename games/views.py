from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Game, Genre
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from .forms import GameForm, GenreForm
from .models import Game
from wishlist.models import Wishlist


class GameListView(ListView):
    model = Game
    template_name = 'games/game_list.html'
    context_object_name = 'games'
    paginate_by = 20

    def get_queryset(self):
        queryset = Game.objects.filter(is_active=True).order_by('-id')

        selected_genres = self.request.GET.getlist('genre')
        selected_ages = self.request.GET.getlist('age_rating')
        search_query = self.request.GET.get('search')

        if selected_genres:
            queryset = queryset.filter(genres__slug__in=selected_genres).distinct()

        if selected_ages:
            queryset = queryset.filter(age_rating__in=selected_ages)

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['age_choices'] = [choice[0] for choice in Game.AGE_RATINGS]

        context['selected_genres'] = self.request.GET.getlist('genre')
        context['selected_ages'] = self.request.GET.getlist('age_rating')

        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['query_string'] = query_params.urlencode()

        return context


class GameDetailView(DetailView):
    model = Game
    template_name = 'games/game_detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаємо відгуки на сторінку гри
        context['reviews'] = self.object.reviews.all().order_by('-created_at')
        return context

@staff_member_required
def game_create(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = GameForm()
    return render(request, 'games/game_form.html', {'form': form, 'title': 'Додавання нової гри'})

@staff_member_required
def game_edit(request, id):
    game = get_object_or_404(Game, id=id)
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = GameForm(instance=game)
    return render(request, 'games/game_form.html', {'form': form, 'title': f'Редагування: {game.title}'})

@staff_member_required
def genre_create(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = GenreForm()
    return render(request, 'games/game_form.html', {'form': form, 'title': 'Додавання нового жанру'})


@staff_member_required
def game_delete(request, id):
    game = get_object_or_404(Game, id=id)
    if request.method == 'POST':
        game.delete()
        return redirect('users:profile')

    return render(request, 'games/game_confirm_delete.html', {'game': game})


@staff_member_required
def genre_delete(request, id):
    genre = get_object_or_404(Genre, id=id)
    if request.method == 'POST':
        genre.delete()
        return redirect('users:profile')
    return render(request, 'games/genre_confirm_delete.html', {'genre': genre})