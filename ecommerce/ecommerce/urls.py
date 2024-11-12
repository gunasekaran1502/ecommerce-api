"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from stores.views import (
    ProductListView, SeasonalProductListView, BulkProductListView, ProductCreateView,
    DiscountListView, PercentageDiscountCreateView, FixedAmountDiscountCreateView,
    OrderCreateView, OrderListView
)

urlpatterns = [
    # Product URLs
    path('products/', ProductListView.as_view(), name='product-list'),
    path('seasonal-products/', SeasonalProductListView.as_view(), name='seasonal-product-list'),
    path('bulk-products/', BulkProductListView.as_view(), name='bulk-product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    
    # Discount URLs
    path('discounts/', DiscountListView.as_view(), name='discount-list'),
    path('discounts/percentage/create/', PercentageDiscountCreateView.as_view(), name='percentage-discount-create'),
    path('discounts/fixed-amount/create/', FixedAmountDiscountCreateView.as_view(), name='fixed-amount-discount-create'),
    
    # Order URLs
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
]
