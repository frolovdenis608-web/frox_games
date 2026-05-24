from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from games.models import Game
from .models import Order, OrderItem
from discounts.models import PromoCode
from decimal import Decimal


def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = Decimal('0.00')

    for game_id, item_data in cart.items():
        game = get_object_or_404(Game, id=game_id)
        price = Decimal(item_data['price'])
        cart_items.append({'game': game, 'price': price})
        total_price += price

    discount_type = request.session.get('discount_type', 'PERCENT')
    discount_value = request.session.get('discount_value', 0)

    if discount_value > 0:
        if discount_type == 'PERCENT':
            total_price = total_price * (Decimal(100 - discount_value) / Decimal(100))
        elif discount_type == 'FIXED':
            total_price = max(Decimal('0.00'), total_price - Decimal(discount_value))

    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'discount_value': discount_value,
        'discount_type': discount_type
    })


def cart_add(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    cart = request.session.get('cart', {})

    if str(game_id) not in cart:
        cart[str(game_id)] = {'price': str(game.get_discounted_price)}
        request.session['cart'] = cart
    return redirect('orders:cart_detail')


def cart_remove(request, game_id):
    cart = request.session.get('cart', {})
    if str(game_id) in cart:
        del cart[str(game_id)]
        request.session['cart'] = cart
    return redirect('orders:cart_detail')


@login_required
def order_create(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('games:game_list')

    total_price = Decimal('0.00')
    items_to_create = []

    for game_id, item_data in cart.items():
        game = get_object_or_404(Game, id=game_id)
        price = Decimal(item_data['price'])
        total_price += price
        items_to_create.append((game, price))

    discount_type = request.session.get('discount_type', 'PERCENT')
    discount_value = request.session.get('discount_value', 0)

    if discount_value > 0:
        if discount_type == 'PERCENT':
            total_price = total_price * (Decimal(100 - discount_value) / Decimal(100))
        elif discount_type == 'FIXED':
            total_price = max(Decimal('0.00'), total_price - Decimal(discount_value))

    order = Order.objects.create(user=request.user, total_price=total_price, status='PENDING')

    wishlist = getattr(request.user, 'wishlist', None)

    for game, price in items_to_create:
        OrderItem.objects.create(order=order, game=game, price=price)
        if wishlist and game in wishlist.games.all():
            wishlist.games.remove(game)

    request.session['cart'] = {}
    if 'discount_value' in request.session:
        del request.session['discount_value']
    if 'discount_type' in request.session:
        del request.session['discount_type']

    return redirect('payments:process_payment', order_id=order.id)