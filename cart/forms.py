from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 100)]


class CartAddProductForm(forms.Form):
    """
    Форма для управления количеством товара
    """
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='Количество товара')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    quantity.widget.attrs.update({'class': 'form-control'})
