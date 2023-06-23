from django import template

from store import models

register = template.Library()


@register.simple_tag()
def get_categories():
    return models.Category.objects.all()
