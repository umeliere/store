from django.shortcuts import render
from django.views.generic import ListView, DetailView
from store.models import Product, Category
from cart.forms import CartAddProductForm
from django.db.models import Q


class ProductsWithDiscountView(ListView):
    """
    The products with the discount view
    """
    template_name = 'store/discount_page.html'
    context_object_name = 'products'
    paginate_by = 12
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Акции'
        return context

    def get_queryset(self):
        return Product.objects.exclude(Q(discount=0) | Q(is_available=False))


class SearchProductsWithDiscountView(ListView):
    """
    The products with the discount after the search view
    """
    template_name = 'store/search_discount_page.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search", '')
        context['search'] = f"search={search}&"
        if not search:
            context["title"] = 'Все товары'
        else:
            context['title'] = f'Товары по запросу: {search}'
        return context

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('search', '')).exclude(
            Q(discount=0) | Q(is_available=False))


class ProductsWithDiscountByCategory(ListView):
    """
    The products with the discount filtered by the categories view
    """
    template_name = 'store/discount_page_by_category.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs['pk']).exclude(
            Q(discount=0) | Q(is_available=False))


class ProductsWithoutDiscountView(ListView):
    """
    The products without any discount view
    """
    template_name = 'store/products_page.html'
    context_object_name = 'products'
    paginate_by = 12
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Продукты'
        return context

    def get_queryset(self):
        return Product.objects.filter(discount=0, is_available=True)


class SearchProductsWithoutDiscountView(ListView):
    """
    The products without any discount after the search view
    """
    template_name = 'store/search_products_page.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search", '')
        context['search'] = f"search={search}&"
        if not search:
            context["title"] = 'Все товары'
        else:
            context['title'] = f'Товары по запросу: {search}'
        return context

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('search', ''), discount=0, is_available=True)


class ProductsWithoutDiscountByCategory(ListView):
    """
    The products without any discount filtered by the categories view
    """
    template_name = 'store/products_page_by_category.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs['pk'], discount=0, is_available=True)


class ProductDetailView(DetailView):
    """
    The product detail view
    """
    template_name = 'store/product.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['cart_product_form'] = CartAddProductForm
        return context


def handler404(request, exception):
    """
    404 error view
    """
    context = {
        'title': 'Страница не найдена: 404',
        'error_message': 'К сожалению такая страница была не найдена, или перемещена',
    }
    return render(request=request, template_name='error/error_page.html', status=404, context=context)


def handler500(request):
    """
    500 error view
    """
    context = {
        'title': 'Ошибка сервера: 500',
        'error_message': 'Внутренняя ошибка сайта, вернитесь на главную страницу сайта'
    }
    return render(request=request, template_name='error/error_page.html', status=500, context=context)


def handler403(request, exception):
    """
    403 error view
    """
    context = {
        'title': 'Ошибка доступа: 403',
        'error_message': 'Доступ к этой странице ограничен',
    }
    return render(request=request, template_name='error/error_page.html', status=403, context=context)
