# wishlist/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from games.models import Game
from .models import Wishlist


@login_required
def wishlist_detail(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'wishlist/wishlist_detail.html', {'wishlist': wishlist})


@login_required
def toggle_wishlist(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if game in wishlist.games.all():
        wishlist.games.remove(game)
    else:
        wishlist.games.add(game)

    return redirect('wishlist:wishlist_detail')