from django.urls import path
from store.views import (
    ProductsWithDiscountView,
    SearchProductsWithDiscountView,
    ProductsWithDiscountByCategory,
    ProductsWithoutDiscountView,
    SearchProductsWithoutDiscountView,
    ProductsWithoutDiscountByCategory,
    ProductDetailView,
)

app_name = 'store'
urlpatterns = [
    # products with some discount
    path('', ProductsWithDiscountView.as_view(), name='discount_page'),
    path('discount_search/', SearchProductsWithDiscountView.as_view(), name='discount_search'),
    path('products/discount_category/<int:pk>/', ProductsWithDiscountByCategory.as_view(),
         name='category_by_product'),
    # products without any discount
    path('products/', ProductsWithoutDiscountView.as_view(), name='products_page'),
    path('products_search/', SearchProductsWithoutDiscountView.as_view(), name='search'),
    path('products/products_category/<int:pk>/', ProductsWithoutDiscountByCategory.as_view(), name='category'),
    # detailed product page
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
