from django.db import models
from django.urls import reverse_lazy


class Product(models.Model):
    """
    The product model
    """
    name = models.CharField(max_length=100, verbose_name='Название товара', unique=True)
    weight = models.FloatField(verbose_name='Масса')
    shelf_time = models.DateField(verbose_name='Срок годности')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    photo = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Скидка для товара', default=0,
                                   blank=True)
    is_available = models.BooleanField(verbose_name='Доступен ли товар?', default=False)
    producer = models.ForeignKey('Producer', on_delete=models.PROTECT)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = "Продукты"
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_discount(self):
        """
        The method that counts the discount of the product
        """
        return self.price * (100 - self.discount) / 100

    def get_absolute_url(self):
        return reverse_lazy('store:product_detail', kwargs={'pk': self.pk})


class Producer(models.Model):
    """
    The producer model
    """
    name = models.CharField(max_length=50, verbose_name='Производитель товара')

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = "Производители"

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    The category model
    """
    name = models.CharField(max_length=50, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
