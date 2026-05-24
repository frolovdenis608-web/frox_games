# payments/views.py
import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import Order
from .models import Payment


@login_required
def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        Payment.objects.create(
            order=order,
            amount=order.total_price,
            method='TEST',
            is_successful=True,
            transaction_id=f"TXN-{uuid.uuid4().hex[:8].upper()}"
        )

        # Оновлюємо статус замовлення
        order.status = 'COMPLETED'
        order.save()

        for item in order.items.all():
            if not item.license_key:

                key_part1 = uuid.uuid4().hex[:5].upper()
                key_part2 = uuid.uuid4().hex[5:10].upper()
                key_part3 = uuid.uuid4().hex[10:15].upper()
                item.license_key = f"{key_part1}-{key_part2}-{key_part3}"
                item.save()

        return redirect('payments:payment_success')

    return render(request, 'payments/checkout.html', {'order': order})


def payment_success(request):
    return render(request, 'payments/success.html')