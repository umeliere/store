from django.views.generic import ListView, DetailView
from store.models import Product, Category
from cart.forms import CartAddProductForm
from django.db.models import Q


class ProductsWithDiscountView(ListView):
    """
    Представление продуктов с акцией
    """
    template_name = 'store/discount_page.html'
    context_object_name = 'products'
    paginate_by = 4
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Акции'
        return context

    def get_queryset(self):
        return Product.objects.exclude(Q(discount=0) | Q(is_available=False))


class SearchProductsWithDiscountView(ListView):
    """
    Представление продуктов с акцией, после поиска
    """
    template_name = 'store/search_discount_page.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        context['search'] = f"search={search}&"
        if not search:
            context["title"] = 'Все товары'
        else:
            context['title'] = f'Товары по запросу: {search}'
        return context

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('search')).exclude(
            Q(discount=0) | Q(is_available=False))


class ProductsWithDiscountByCategory(ListView):
    """
    Представление продуктов с акцией по определенной категории
    """
    template_name = 'store/discount_page_by_category.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs['pk']).exclude(
            Q(discount=0) | Q(is_available=False))


class ProductsWithoutDiscountView(ListView):
    """
    Представление продуктов без акций
    """
    template_name = 'store/products_page.html'
    context_object_name = 'products'
    paginate_by = 4
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Продукты'
        return context

    def get_queryset(self):
        return Product.objects.filter(discount=0, is_available=True)


class SearchProductsWithoutDiscountView(ListView):
    """
    Представление продуктов без акций после поиска
    """
    template_name = 'store/search_products_page.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        context['search'] = f"search={search}&"
        if not search:
            context["title"] = 'Все товары'
        else:
            context['title'] = f'Товары по запросу: {search}'
        return context

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('search'), discount=0, is_available=True)


class ProductsWithoutDiscountByCategory(ListView):
    """
    Представление продуктов без акций по определенной категории
    """
    template_name = 'store/products_page_by_category.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs['pk'], discount=0, is_available=True)


class ProductDetailView(DetailView):
    """
    Представление определенного продукта
    """
    template_name = 'store/product.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['cart_product_form'] = CartAddProductForm
        return context
