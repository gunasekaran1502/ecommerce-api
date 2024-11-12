from rest_framework import serializers
from .models import Product, SeasonalProduct, BulkProduct, PercentageDiscount, FixedAmountDiscount, Order,Discount

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'base_price']

class SeasonalProductSerializer(ProductSerializer):
    class Meta:
        model = SeasonalProduct
        fields = ['id', 'name', 'base_price', 'seasonal_discount']

class BulkProductSerializer(ProductSerializer):
    class Meta:
        model = BulkProduct
        fields = ['id', 'name', 'base_price', 'bulk_discount', 'bulk_quantity_threshold']

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id']

class PercentageDiscountSerializer(DiscountSerializer):
    class Meta:
        model = PercentageDiscount
        fields = ['id', 'percentage']

class FixedAmountDiscountSerializer(DiscountSerializer):
    class Meta:
        model = FixedAmountDiscount
        fields = ['id', 'amount']


from rest_framework import serializers
from .models import Order, Product, PercentageDiscount

class OrderSerializer(serializers.ModelSerializer):
    # Use PrimaryKeyRelatedField for the product (expects a product ID)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    # Discount as a PrimaryKeyRelatedField (ID of discount)
    discount = serializers.PrimaryKeyRelatedField(queryset=PercentageDiscount.objects.all(), required=False)
    
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'product', 'discount', 'quantity', 'total_price']

    def get_total_price(self, obj):
        # Calculate the total price dynamically
        product_price = obj.product.get_price()  # Assuming get_price is implemented in Product
        quantity = obj.quantity
        discount = obj.discount
        
        # If a discount exists, apply it
        if discount:
            if isinstance(discount, PercentageDiscount):
                discount_value = discount.percentage / 100
                total_price = (product_price * quantity) * (1 - discount_value)
            else:
                total_price = (product_price * quantity) - discount.amount
        else:
            total_price = product_price * quantity
        
        return total_price

    def create(self, validated_data):
        # No need to manually fetch the product; the serializer will do that.
        order = Order.objects.create(**validated_data)
        return order