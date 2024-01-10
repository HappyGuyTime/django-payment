import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Item, Order
from .services import create_stripe_tax_rate, create_stripe_coupon, create_stripe_line_items


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='https://example.com/success',
    )

    return JsonResponse({'session_id': session.id})


def get_item_page(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    context = {'item': item}
    return render(request, 'stripePayment/item.html', context)


def create_stripe_session_order(request, order_id):
    order = get_object_or_404(Order.objects.select_related('discount', 'tax').prefetch_related('items'), pk=order_id)
    tax_rate = create_stripe_tax_rate(tax=order.tax)
    line_items = create_stripe_line_items(items=order.items.all(), tax_rate_id=tax_rate.id)
    coupon = create_stripe_coupon(discount=order.discount)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='https://example.com/success',
        discounts=[
        {
            'coupon': coupon.id,
        },
        ]
    )

    return JsonResponse({'session_id': session.id})


def get_order_page(request, order_id):
    order = get_object_or_404(Order.objects.select_related('discount', 'tax').prefetch_related('items'), pk=order_id)
    context = {'order': order}
    return render(request, 'stripePayment/order.html', context)


def create_stripe_payment_intent_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    intent = stripe.PaymentIntent.create(
        amount=int(item.price * 100),
        currency=item.currency,
        payment_method_types=['card'],
    )

    return JsonResponse({'intent': intent})


def get_item_intent_page(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    context = {'item': item}
    return render(request, 'stripePayment/item_intent.html', context)


def create_stripe_payment_intent_order(request, order_id):
    order = get_object_or_404(Order.objects.select_related('discount', 'tax').prefetch_related('items'), pk=order_id)
    total_amount = float(order.total_amount)
    discount_amount = total_amount * (order.discount.percent_off / 100)
    total_amount -= discount_amount
    tax_amount = total_amount * (order.tax.percentage / 100)

    total_amount += tax_amount

    intent = stripe.PaymentIntent.create(
        payment_method_types=['card'],
        amount=int(total_amount * 100),
        currency='usd',
        payment_method_options={
            'card': {
                'request_three_d_secure': 'any'
            },
        },
        metadata={
            'order_id': order_id
        },
    )

    return JsonResponse({'intent': intent})
