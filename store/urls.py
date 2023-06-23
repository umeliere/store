from django.urls import path
from store import views

urlpatterns = [
    path('', views.GoodsWithDiscountPageView.as_view(), name='discount_page'),
    path('products/', views.GoodsPageView.as_view(), name='products_page'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('search/', views.SearchViewOfGoods.as_view(), name='search'),
    path('discount_search/', views.SearchViewOfGoodsWithDiscount.as_view(), name='discount_search'),
    path('goods/category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('products/discount_category/<int:pk>/', views.CategoryViewByProducts.as_view(), name='category_by_product'),
]
