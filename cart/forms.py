from django import forms
from cart.models import CartItem


class CartAddProductForm(forms.ModelForm):
    """
    the form for the quantity of product
    """
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'] = forms.IntegerField(min_value=1, max_value=99, label="Количество",
                                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CartItem
        fields = ('quantity',)
