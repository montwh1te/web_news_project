from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='replace_underscore')
def replace_underscore(value):
    return value.replace("_", " ")