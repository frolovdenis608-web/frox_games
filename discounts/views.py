from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from .models import PromoCode
from .forms import PromoCodeForm


@require_POST
def apply_promocode(request):
    code_text = request.POST.get('code', '').strip()
    try:
        promocode = PromoCode.objects.get(code__iexact=code_text)
        if promocode.is_valid():
            # Записуємо обидва параметри в сесію
            request.session['discount_type'] = promocode.discount_type
            request.session['discount_value'] = promocode.value

            if promocode.discount_type == 'PERCENT':
                messages.success(request, f"Промокод успішно застосовано! Знижка {promocode.value}%")
            else:
                messages.success(request, f"Промокод успішно застосовано! Знижка {promocode.value} грн")
        else:
            messages.error(request, "Термін дії промокоду закінчився або він неактивний.")
    except PromoCode.DoesNotExist:
        messages.error(request, "Такого промокоду не існує.")

    return redirect('orders:cart_detail')


@staff_member_required
def promocode_create(request):
    if request.method == 'POST':
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Промокод успішно створено!")
            return redirect('users:profile')
    else:
        form = PromoCodeForm()
    return render(request, 'games/game_form.html', {'form': form, 'title': 'Створення нового промокоду'})


@staff_member_required
def promocode_delete(request, id):
    promocode = get_object_or_404(PromoCode, id=id)
    if request.method == 'POST':
        promocode.delete()
        messages.success(request, "Промокод видалено!")
        return redirect('users:profile')
    return render(request, 'discounts/promocode_confirm_delete.html', {'promocode': promocode})