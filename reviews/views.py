from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from games.models import Game
from .models import Review

@login_required
@require_POST
def add_review(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    rating = request.POST.get('rating')
    comment = request.POST.get('comment', '')

    if rating:
        Review.objects.update_or_create(
            user=request.user,
            game=game,
            defaults={'rating': int(rating), 'comment': comment}
        )
    return redirect('games:game_detail', slug=game.slug)
