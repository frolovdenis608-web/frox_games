from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from orders.models import Order
from games.models import Game, Genre
from discounts.models import PromoCode
from .forms import CustomUserCreationForm, ProfileEditForm
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('games:game_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('games:game_list')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('games:game_list')

@login_required
def profile_view(request):
    if request.user.is_staff:
        search_query = request.GET.get('search', '')
        genre_filter = request.GET.get('genre', '')

        games = Game.objects.all()

        if search_query:
            games = games.filter(title__icontains=search_query)
        if genre_filter:
            games = games.filter(genres__name=genre_filter)

        genres = Genre.objects.all()
        promocodes = PromoCode.objects.all().order_by('-id')

        return render(request, 'users/profile.html', {
            'games': games,
            'genres': genres,
            'promocodes': promocodes,
            'is_admin': True,
            'search_query': search_query,
            'current_genre': genre_filter
        })
    else:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'users/profile.html', {
            'orders': orders,
            'is_admin': False
        })


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Особисті дані успішно оновлено!")
            return redirect('users:profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()

            update_session_auth_hash(request, form.user)
            messages.success(request, "Пароль успішно змінено!")
            return redirect('users:profile')
    else:
        form = PasswordChangeForm(user=request.user)

    for field in form.fields.values():
        field.widget.attrs.update({
            'style': 'background: #222; color: white; padding: 8px; border: 1px solid #555; width: 100%; box-sizing: border-box;'
        })

    return render(request, 'users/password_change.html', {'form': form})