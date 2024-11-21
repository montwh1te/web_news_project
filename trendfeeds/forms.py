# **IMPORTAÇÕES DO DJANGO**
from django import forms  
    # Importa o módulo `forms` do Django, que permite criar formulários baseados em modelos ou personalizados.

# **IMPORTAÇÕES INTERNAS**
from .models import Comentario  
    # Importa o modelo `Comentario` do aplicativo atual para ser usado no formulário.

class ComentarioForm(forms.ModelForm):  # Define um formulário baseado no modelo `Comentario`.
    class Meta:  
        # Classe interna usada para configurar o formulário.
        model = Comentario  
            # Especifica que este formulário está vinculado ao modelo `Comentario`.
        fields = ['comentario'] 
            # Define os campos do modelo que estarão disponíveis no formulário; aqui, apenas o campo `comentario` será incluído.
