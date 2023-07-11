from django.urls import path
from orders.views import OrderCreateView, SuccessfulPurchaseView

app_name = 'orders'
urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('success/', SuccessfulPurchaseView.as_view(), name='success')
]
