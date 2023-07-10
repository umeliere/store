from django import forms

from orders.models import Order


class OrderCreateForm(forms.ModelForm):
    """
    Форма оформления заказа
    """
    class Meta:
        model = Order
        fields = ['full_name', 'cc_number', 'cc_expiry', 'cc_code']
