from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, FormView
from django.core.exceptions import ObjectDoesNotExist

from store.models import Product
from cart.models import Cart, CartItem
from cart.forms import CartAddProductForm


class CartDetailView(LoginRequiredMixin, ListView):
    """
    Представление корзины пользователя
    """
    model = Cart
    template_name = 'cart/cart.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'
        if Cart.objects.filter(user=self.request.user):
            context['cart'] = Cart.objects.get(user=self.request.user)
            context['items'] = context['cart'].cartitem_set.all().select_related('product')
            context['get_total_discount'] = context['cart'].get_total_discount(context['cart'])
            try:
                context['get_total_cost'] = context['cart'].get_total_cost(
                    context['cart']) - context['get_total_discount']
            except TypeError:
                pass

            for item in context['items']:
                cart_item = CartAddProductForm(initial={'quantity': item.quantity, 'update': True})
                setattr(item, 'update_quantity_form', cart_item)

        return context


class CartAddView(FormView):
    """
    Представление для добавления товара в корзину
    """
    form_class = CartAddProductForm

    def form_valid(self, form):
        cart = Cart.get_card(self.request.user)
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        quantity = form.cleaned_data['quantity']
        status = form.cleaned_data['update']
        try:
            item = cart.cartitem_set.get(product=product)
            if not status:
                item.quantity += quantity
                item.save()
            else:
                item.quantity = quantity
                item.save()
        except ObjectDoesNotExist:
            cart.cartitem_set.create(quantity=quantity, product=product)
            cart.save()

        return redirect('cart:cart_detail')


class CartItemDeleteView(DeleteView):
    """
    Представление удаления товара из корзины
    """
    template_name = 'cart/cart.html'

    def get(self, request, *args, **kwargs):
        cart = Cart.get_card(self.request.user)
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        CartItem.objects.get(cart=cart, product=product).delete()
        return redirect('cart:cart_detail')
