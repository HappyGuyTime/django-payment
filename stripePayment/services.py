import stripe


def create_stripe_tax_rate(tax):
    return stripe.TaxRate.create(
        display_name='VAT',
        description='Value Added Tax',
        jurisdiction='USA',
        percentage=tax.percentage,
        inclusive=False,
        )


def create_stripe_coupon(discount):
    return stripe.Coupon.create(
        percent_off=discount.percent_off,
        duration='once',  
        name=f'{discount.percent_off}% OFF',
        )


def create_stripe_line_items(items, tax_rate_id):
    line_items = []

    for item in items:
        line_item = {
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
            'tax_rates': [tax_rate_id],
        }
        line_items.append(line_item)

    return line_items