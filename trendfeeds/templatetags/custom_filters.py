# **IMPORTAÇÕES DO DJANGO**
from django import template  
    # Importa o módulo `template`, que permite criar tags e filtros personalizados no Django.
from django.template.defaultfilters import slugify  
    # Importa o filtro padrão `slugify`, que converte uma string em um formato de slug (amigável para URLs).




register = template.Library()  
# Cria uma instância de `Library` para registrar novos filtros ou tags personalizados.

@register.filter  
# Registra a função como um filtro customizado que pode ser usado nos templates.
def slugify_with_underscore(value):  
    """Transforma uma string em slug e substitui hífens por underscores."""  
        # Descrição da funcionalidade do filtro.
    return slugify(value).replace('-', '_')  
        # Converte a string em um slug usando `slugify` e substitui os hífens ('-') por underscores ('_').
