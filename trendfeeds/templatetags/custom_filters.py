from django import template
from django.template.defaultfilters import slugify

register = template.Library()

@register.filter
def slugify_with_underscore(value):
    """Transforma uma string em slug e substitui hífens por underscores."""
    return slugify(value).replace('-', '_')

