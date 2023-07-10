from decimal import Decimal
from django.conf import settings
from store import models


class Cart(object):
    """
    Класс для корзины
    """
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_pk = str(product.pk)
        if product_pk not in self.cart:
            self.cart[product_pk] = {'quantity': 0,
                                     'price': str(product.price),
                                     'weight': float(product.weight),
                                     'discount': str(product.discount),
                                     }
        if update_quantity:
            self.cart[product_pk]['quantity'] = quantity
        else:
            self.cart[product_pk]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Обновление сессии корзины
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_pk = str(product.pk)
        if product_pk in self.cart:
            del self.cart[product_pk]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_pks = self.cart.keys()
        products = models.Product.objects.filter(pk__in=product_pks)
        for product in products:
            self.cart[str(product.pk)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['discount'] = Decimal(item['discount'])
            item['total_weight'] = item['weight'] * item['quantity']
            if item['discount'] != 0:
                get_discount = round(item['price'] * (100 - item['discount']) / 100, 2)
                item['total_price'] = get_discount * item['quantity']
            else:
                item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_discount(self):
        """
        Подсчет стоимости скидки в корзине.
        """
        return sum((item['price'] - round(Decimal(item['price'] * (100 - Decimal(item['discount'])) / 100), 2)) *
                   item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values()) - self.get_total_discount()

    def clear(self):
        """
        Удаление корзины из сессии
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
