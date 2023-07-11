from django.urls import path
from cart.views import CartDetailView, CartAddView, CartRemoveView
from django.views.decorators.http import require_POST

app_name = 'cart'
urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:pk>/', require_POST(CartAddView.as_view()), name='cart_add'),
    path('remove/<int:pk>/', CartRemoveView.as_view(), name='cart_remove'),
]
