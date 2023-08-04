from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from orders.models import OrderItem
from orders.forms import OrderCreateForm
from cart.models import Cart, CartItem


class OrderCreateView(LoginRequiredMixin, CreateView):
    """
    Place the order view
    """
    login_url = reverse_lazy('users:login')
    form_class = OrderCreateForm
    template_name = 'orders/create.html'
    success_url = reverse_lazy('orders:success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление заказа'
        context['cart'], _ = Cart.objects.get_or_create(user=self.request.user)
        try:
            context['get_total_cost'] = context['cart'].get_total_cost() - context['cart'].get_total_discount()
        except TypeError:
            context['get_total_cost'] = context['cart'].get_total_cost()
        context['items'] = CartItem.objects.filter(cart=context['cart']).select_related('product')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        with transaction.atomic():
            form.instance.user = self.request.user
            items = context['items']
            for item in items:
                OrderItem.objects.create(order=form.save(),
                                         product=item.product,
                                         price=item.product.get_discount(),
                                         quantity=item.quantity)

            items.delete()
        return super(OrderCreateView, self).form_valid(form)


class SuccessfulPurchaseView(TemplateView):
    """
    Successful placed the order view
    """
    template_name = "orders/successful_purchase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вы успешно оформили заказ!'
        return context
