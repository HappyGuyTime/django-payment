from django.contrib import admin
from .models import Item, Order, Discount, Tax


admin.site.register(Item)
admin.site.register(Discount)
admin.site.register(Tax)


class ItemInline(admin.TabularInline):
    model = Order.items.through
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (ItemInline, )
    exclude = ('items', )