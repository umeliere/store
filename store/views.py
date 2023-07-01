from django.views.generic import ListView, DetailView
from store import models
from cart.forms import CartAddProductForm


# products with some discount
class ProductsWithDiscountView(ListView):
    template_name = 'store/discount_page.html'
    context_object_name = 'products'
    paginate_by = 4
    model = models.Product

    def get_queryset(self):
        return models.Product.objects.exclude(discount=0)


class SearchProductsWithDiscountView(ListView):
    template_name = 'store/search_discount_page.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        return models.Product.objects.filter(name__icontains=self.request.GET.get('search')).exclude(discount=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = f"search={self.request.GET.get('search')}&"
        return context


class ProductsWithDiscountByCategory(ListView):
    template_name = 'store/discount_page_by_category.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = models.Category.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return models.Product.objects.filter(category_id=self.kwargs['pk']).exclude(discount=0)


# products without any discount
class ProductsWithoutDiscountView(ListView):
    template_name = 'store/products_page.html'
    context_object_name = 'products'
    paginate_by = 4
    model = models.Product

    def get_queryset(self):
        return models.Product.objects.filter(discount=0)


class SearchProductsWithoutDiscountView(ListView):
    template_name = 'store/search_products_page.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        return models.Product.objects.filter(name__icontains=self.request.GET.get('search'), discount=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = f"search={self.request.GET.get('search')}&"
        return context


class ProductsWithoutDiscountByCategory(ListView):
    template_name = 'store/products_page_by_category.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = models.Category.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return models.Product.objects.filter(category_id=self.kwargs['pk'], discount=0)


# detailed product page
class ProductDetailView(DetailView):
    template_name = 'store/product.html'
    model = models.Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context
