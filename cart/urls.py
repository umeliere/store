from django.urls import path
from django.views.decorators.http import require_POST

from cart.views import CartAddView, CartDetailView, CartItemDeleteView

app_name = 'cart'
urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('delete/<int:pk>/', CartItemDeleteView.as_view(), name='cart_remove'),
    path('add/<int:pk>/', require_POST(CartAddView.as_view()), name='cart_add')
]
