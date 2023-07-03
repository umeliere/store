from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin

from store import models
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


class OrderCreateView(SuccessMessageMixin, CreateView):
    form_class = OrderCreateForm
    template_name = 'orders/create.html'
    success_url = reverse_lazy('orders:success')

    def form_valid(self, form):
        form.instance.user = self.request.user
        order = form.save()
        cart = Cart(self.request)
        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])

        cart.clear()
        return super(OrderCreateView, self).form_valid(form)

    def get_queryset(self):
        return models.Product.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context


class SuccessfulPurchaseView(TemplateView):
    template_name = "orders/successful_purchase.html"