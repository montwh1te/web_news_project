from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, class_name):
    """
    Adiciona uma classe CSS a um campo de formulário.
    """
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={'class': class_name})
    return field  # Retorna o campo original se não tiver 'as_widget'


@register.filter(name='replace_underscore')
def replace_underscore(value):
    return value.replace("_", " ")