from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, FormView

from store.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm


class CartAddView(FormView):
    """
    Представление для добавления товара в корзину
    """
    model = Product
    template_name = 'cart/cart.html'
    form_class = CartAddProductForm

    def form_valid(self, form):
        cart = Cart(self.request)
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        clean_data = form.cleaned_data
        cart.add(product=product,
                 quantity=clean_data['quantity'],
                 update_quantity=clean_data['update'])

        return redirect('cart:cart_detail')


class CartRemoveView(DeleteView):
    """
    Представление удаления товара из корзины
    """
    template_name = 'cart/cart.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, pk=kwargs['pk'])
        cart.remove(product)
        return redirect('cart:cart_detail')


class CartDetailView(ListView):
    """
    Представление корзины пользователя
    """
    model = Product
    form_class = CartAddProductForm
    template_name = 'cart/cart.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        context['title'] = 'Корзина'
        for item in context['cart']:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})

        return context
