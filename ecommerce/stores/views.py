from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, SeasonalProduct, BulkProduct, PercentageDiscount, FixedAmountDiscount, Order
from .serializers import (
    ProductSerializer,
    SeasonalProductSerializer,
    BulkProductSerializer,
    PercentageDiscountSerializer,
    FixedAmountDiscountSerializer,
    OrderSerializer
)

# Product Views
class ProductListView(APIView):
    """
    View to list all products.
    """
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class SeasonalProductListView(APIView):
    """
    View to list all seasonal products.
    """
    def get(self, request, *args, **kwargs):
        seasonal_products = SeasonalProduct.objects.all()
        serializer = SeasonalProductSerializer(seasonal_products, many=True)
        return Response(serializer.data)

class  BulkProductListView(APIView):
    """
    View to create a new bulk product.
    """
    def post(self, request, *args, **kwargs):
        # Get the data from the request
        data = request.data
        
        # Initialize the serializer with the provided data
        serializer = BulkProductSerializer(data=data)
        
        # Check if the data is valid
        if serializer.is_valid():
            # Save the new bulk product to the database
            serializer.save()
            
            # Return the serialized data with HTTP 201 Created status
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # If data is invalid, return errors with HTTP 400 Bad Request status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductCreateView(APIView):
    """
    View to create a new product.
    """
    def post(self, request, *args, **kwargs):
        data = request.data
        if data.get('seasonal_discount'):
            serializer = SeasonalProductSerializer(data=data)
        elif data.get('bulk_discount'):
            serializer = BulkProductSerializer(data=data)
        else:
            serializer = ProductSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Discount Views
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PercentageDiscount, FixedAmountDiscount
from .serializers import PercentageDiscountSerializer, FixedAmountDiscountSerializer

class DiscountListView(APIView):
    """
    View to list all discounts (both percentage and fixed amount).
    """
    def get(self, request, *args, **kwargs):
        # Query the two different discount models separately
        percentage_discounts = PercentageDiscount.objects.all()
        fixed_amount_discounts = FixedAmountDiscount.objects.all()

        # Serialize the results separately
        percentage_serializer = PercentageDiscountSerializer(percentage_discounts, many=True)
        fixed_amount_serializer = FixedAmountDiscountSerializer(fixed_amount_discounts, many=True)

        # Combine the serialized data from both models
        all_discounts = percentage_serializer.data + fixed_amount_serializer.data

        # Return the combined data as a response
        return Response(all_discounts)
    


class PercentageDiscountCreateView(APIView):
    """
    View to create a percentage discount.
    """
    def post(self, request, *args, **kwargs):
        serializer = PercentageDiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FixedAmountDiscountCreateView(APIView):
    """
    View to create a fixed amount discount.
    """
    def post(self, request, *args, **kwargs):
        serializer = FixedAmountDiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Order Views
class OrderCreateView(APIView):
    """
    View to create a new order.
    """
    def post(self, request, *args, **kwargs):
        # Initialize the serializer with the incoming request data
        serializer = OrderSerializer(data=request.data)
        
        # Check if the provided data is valid
        if serializer.is_valid():
            # Save the order and return the serialized order data
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        
        # If validation fails, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListView(APIView):
    """
    View to list all orders with detailed product and discount information.
    """
    def get(self, request, *args, **kwargs):
        # Get all orders from the database
        orders = Order.objects.all()
        
        # Serialize the list of orders
        serializer = OrderSerializer(orders, many=True)
        
        # Return the serialized order data with detailed product and discount
        return Response(serializer.data, status=status.HTTP_200_OK)