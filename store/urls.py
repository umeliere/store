from django.urls import path
from store import views

urlpatterns = [
    # products with some discount
    path('', views.ProductsWithDiscountView.as_view(), name='discount_page'),
    path('discount_search/', views.SearchProductsWithDiscountView.as_view(), name='discount_search'),
    path('products/discount_category/<int:pk>/', views.ProductsWithDiscountByCategory.as_view(),
         name='category_by_product'),
    # products without any discount
    path('products/', views.ProductsWithoutDiscountView.as_view(), name='products_page'),
    path('products_search/', views.SearchProductsWithoutDiscountView.as_view(), name='search'),
    path('products/products_category/<int:pk>/', views.ProductsWithoutDiscountByCategory.as_view(), name='category'),
    # detailed product page
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
]
