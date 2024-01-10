from django.urls import path
from django.views.generic import TemplateView

from .views import (
    create_stripe_session_item,  get_item_page, 
    create_stripe_session_order, get_order_page, 
    create_stripe_payment_intent_item, get_item_intent_page,
    create_stripe_payment_intent_order,
    )


urlpatterns = [
    path('buy/<int:item_id>/', create_stripe_session_item, name='stripe_session_item'),
    path('buy-intent/<int:item_id>/', create_stripe_payment_intent_item, name='stripe_payment_intent_item'),
    path('item/<int:item_id>/', get_item_page, name='get_item_page'),
    path('item-intent/<int:item_id>/', get_item_intent_page, name='get_item_intent_page'),
    path('order/<int:order_id>/', get_order_page, name='get_order_page'),
    path('buy-order/<int:order_id>/', create_stripe_session_order, name='stripe_session_order'),
    path('buy-order-intent/<int:order_id>/', create_stripe_payment_intent_order, name='stripe_payment_intent_order'),
    path('card-form/', TemplateView.as_view(template_name='stripePayment/card_form.html'), name='card_form'),
    path('payment-success/', TemplateView.as_view(template_name='stripePayment/payment_success.html'), name='payment_success'),
]