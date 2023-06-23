from django.views.generic import ListView, DetailView
from store import models


# products with some discount
class GoodsWithDiscountPageView(ListView):
    template_name = 'store/index.html'
    context_object_name = 'products'
    paginate_by = 4
    model = models.Product

    def get_queryset(self):
        return models.Product.objects.exclude(discount=0)


class SearchViewOfGoodsWithDiscount(ListView):
    template_name = 'store/search_of_goods_with_discount.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        return models.Product.objects.filter(name__icontains=self.request.GET.get('search')).exclude(discount=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = f"search={self.request.GET.get('search')}&"
        return context


class CategoryViewByProducts(ListView):
    template_name = 'store/products_by_category.html'
    context_object_name = 'products'
    paginate_by = 1

    def get_queryset(self):
        return models.Product.objects.filter(category_id=self.kwargs['pk']).exclude(discount=0)


# products without any discount
class GoodsPageView(ListView):
    template_name = 'store/goods.html'
    context_object_name = 'goods'
    paginate_by = 4
    model = models.Product

    def get_queryset(self):
        return models.Product.objects.filter(discount=0)


class SearchViewOfGoods(ListView):
    template_name = 'store/search_of_goods.html'
    context_object_name = 'goods'
    paginate_by = 4

    def get_queryset(self):
        return models.Product.objects.filter(name__icontains=self.request.GET.get('search'), discount=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = f"search={self.request.GET.get('search')}&"
        return context


class CategoryView(ListView):
    template_name = 'store/goods_by_category.html'
    context_object_name = 'goods'
    paginate_by = 2

    def get_queryset(self):
        return models.Product.objects.filter(category_id=self.kwargs['pk'], discount=0)


# detailed product page
class ProductDetailView(DetailView):
    template_name = 'store/product.html'
    model = models.Product
    context_object_name = 'product'
