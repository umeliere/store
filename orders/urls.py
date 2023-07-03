from django.urls import path
from orders import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('success/', views.SuccessfulPurchaseView.as_view(), name='success')
]
