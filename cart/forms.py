from django import forms
from cart.models import CartItem


class CartAddProductForm(forms.ModelForm):
    """
    Форма для управления количеством товара
    """
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    class Meta:
        model = CartItem
        fields = ('quantity',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
