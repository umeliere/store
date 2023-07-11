from django import template

from store.models import Category, Producer

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_producers():
    return Producer.objects.all()
