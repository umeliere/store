from django.urls import path
from cart import views
from django.views.decorators.http import require_POST

app_name = 'cart'
urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:pk>/', require_POST(views.CartAddView.as_view()), name='cart_add'),
    path('remove/<int:pk>/', views.CartRemoveView.as_view(), name='cart_remove'),
]
