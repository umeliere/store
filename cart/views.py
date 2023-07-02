from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from store import models
from .cart import Cart
from cart import forms


@require_POST
def cart_add(request, pk):
    cart = Cart(request)
    product = get_object_or_404(models.Product, pk=pk)
    form = forms.CartAddProductForm(request.POST)
    if form.is_valid():
        clean_data = form.cleaned_data
        cart.add(product=product,
                 quantity=clean_data['quantity'],
                 update_quantity=clean_data['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, pk):
    cart = Cart(request)
    product = get_object_or_404(models.Product, pk=pk)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = forms.CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/cart.html', {'cart': cart})
