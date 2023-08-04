from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, FormView

from store.models import Product
from cart.models import Cart, CartItem
from cart.forms import CartAddProductForm


class CartDetailView(LoginRequiredMixin, ListView):
    """
    The user cart view
    """
    model = Cart
    template_name = 'cart/cart.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'
        context['cart'], _ = Cart.objects.get_or_create(user=self.request.user)
        context['items'] = CartItem.objects.filter(cart=context['cart']).select_related('product')
        if context['items']:
            context['get_total_discount'] = context['cart'].get_total_discount()
            context['get_total_cost'] = context['cart'].get_total_cost()

            for item in context['items']:
                cart_item = CartAddProductForm(initial={'quantity': item.quantity, 'update': True})
                setattr(item, 'update_quantity_form', cart_item)

        return context


class CartAddView(LoginRequiredMixin, FormView):
    """
    Add the product to the cart view
    """
    form_class = CartAddProductForm
    redirect_field_name = 'cart_detail'

    def form_valid(self, form):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        quantity = form.cleaned_data['quantity']
        status = form.cleaned_data['update']
        item, _ = CartItem.objects.get_or_create(product=product, cart=cart)

        if status:
            item.quantity = quantity
            item.save()
        else:
            item.quantity += quantity
            item.save()

        return redirect('cart:cart_detail')


class CartItemDeleteView(DeleteView):
    """
    Remove the product from the cart view
    """
    template_name = 'cart/cart.html'

    def get(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        CartItem.objects.get(cart=cart, product=product).delete()
        return redirect('cart:cart_detail')
