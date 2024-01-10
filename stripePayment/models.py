from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(Item, related_name='orders')
    discount = models.ForeignKey('Discount', related_name='orders', on_delete=models.SET_NULL, null=True)
    tax = models.ForeignKey('Tax', related_name='orders', on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"Order №{self.pk}"

    @property
    def total_amount(self):
        total = sum(item.price for item in self.items.all())
        return total


class Discount(models.Model):
    percent_off = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.percent_off} %"


class Tax(models.Model):
    percentage = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.percentage} %"