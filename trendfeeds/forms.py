''' **IMPORTAÇÕES DO DJANGO**  '''
# Importa o módulo `forms` do Django, que permite criar formulários baseados em modelos ou personalizados.
from django import forms  


''' **IMPORTAÇÕES INTERNAS**  '''
# Importa o modelo `Comentario` e `Noticias` do aplicativo atual para serem usados no formulário.
from .models import Comentario, Noticias  




# Define um formulário baseado no modelo `Comentario`.
class ComentarioForm(forms.ModelForm):  
    class Meta:  


        # Classe interna usada para configurar o formulário.
        model = Comentario  

        # Especifica que este formulário está vinculado ao modelo `Comentario`.
        # Define os campos do modelo que estarão disponíveis no formulário; aqui, apenas o campo `comentario` será incluído.
        fields = ['comentario'] 




# Define um formulário baseado no modelo `Noticias` para edição.
class EditarNoticiaForm(forms.ModelForm):
    class Meta:

        # Classe interna usada para configurar o formulário.
        model = Noticias

        # Define os campos que podem ser editados no formulário.
        fields = ['titulo', 'descricao', 'autor', 'link', 'categorias']  



class NoticiasForm(forms.ModelForm):
    
    imagens = forms.FileField(widget=forms.ClearableFileInput, required=False)

    class Meta:
        model = Noticias
        fields = ['titulo', 'descricao', 'autor', 'link', 'categorias']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o título'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite a descrição'}),
            'autor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Autor da notícia'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link da notícia'}),
            'categorias': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'autor': 'Autor',
            'link': 'Link',
            'categorias': 'Categorias',
        }