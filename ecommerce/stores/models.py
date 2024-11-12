from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Product Management

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


    def get_price(self):
        return self.base_price


class SeasonalProduct(Product):
    seasonal_discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.10)

    def get_price(self):
        return self.base_price * (1 - self.seasonal_discount)


class BulkProduct(Product):
    bulk_discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.15)
    bulk_quantity_threshold = models.IntegerField(default=10)

    def get_price(self, quantity=1):
        if quantity >= self.bulk_quantity_threshold:
            return self.base_price * (1 - self.bulk_discount)
        return self.base_price

# Discount Management

class Discount(models.Model):
    class Meta:
        abstract = True

    def apply_discount(self, price):
        raise NotImplementedError("Subclasses must implement apply_discount method.")


class PercentageDiscount(Discount):
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def apply_discount(self, price):
        return price * (1 - self.percentage)


class FixedAmountDiscount(Discount):
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def apply_discount(self, price):
        return max(price - self.amount, 0)

# Order Management

class Order(models.Model):
    product_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='product_type')
    product_id = models.PositiveIntegerField()
    product = GenericForeignKey('product_content_type', 'product_id')

   

    discount_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='discount_type', null=True, blank=True)
    discount_id = models.PositiveIntegerField(null=True, blank=True)
    discount = GenericForeignKey('discount_content_type', 'discount_id')

    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def calculate_total_price(self):
        product_price = self.product.get_price(self.quantity) if isinstance(self.product, BulkProduct) else self.product.get_price()
        total_price = product_price * self.quantity

        if self.discount:
            total_price = self.discount.apply_discount(total_price)

        return total_price
