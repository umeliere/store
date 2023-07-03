from django import forms
from phonenumber_field.formfields import PhoneNumberField

from orders.models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'phone', 'city']
