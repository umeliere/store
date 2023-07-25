from django import template

from store.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    """
    get all the categories
    """
    return Category.objects.all()
