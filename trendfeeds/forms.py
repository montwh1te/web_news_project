''' **IMPORTAÇÕES DO DJANGO**  '''
# Importa o módulo `forms` do Django, que permite criar formulários baseados em modelos ou personalizados.
from django import forms  



''' **IMPORTAÇÕES INTERNAS**  '''
# Importa o modelo `Comentario` e `Noticias` do aplicativo atual para serem usados no formulário.
from .models import Comentario, Noticias, Categoria 




# Define um formulário baseado no modelo `Comentario`.
class ComentarioForm(forms.ModelForm):  
    # Configurações específicas do formulário.
    class Meta:  
        # Classe interna usada para configurar o formulário.
        model = Comentario  
        
        # Especifica que este formulário está vinculado ao modelo `Comentario`.
        # Define os campos do modelo que estarão disponíveis no formulário; aqui, apenas o campo `comentario` será incluído.
        fields = ['comentario'] 





# Define um formulário baseado no modelo `Noticias` para edição.
class EditarNoticiaForm(forms.ModelForm):
    # Configurações específicas do formulário.
    class Meta:
        # Classe interna usada para configurar o formulário.
        model = Noticias

        # Define os campos que podem ser editados no formulário.
        fields = ['titulo', 'descricao', 'autor', 'link', 'categorias']  





# Define um formulário para criar notícias, incluindo a possibilidade de upload de imagens.
class NoticiasForm(forms.ModelForm):
    # Adiciona um campo personalizado para upload de imagens.
    # O widget `ClearableFileInput` é usado para permitir uploads e exclusões de arquivos.
    imagens = forms.FileField(widget=forms.ClearableFileInput, required=False)

    # Configurações específicas do formulário.
    class Meta:
        # Classe interna usada para configurar o formulário.
        model = Noticias

        # Define os campos que estarão disponíveis no formulário.
        fields = ['titulo', 'descricao', 'autor', 'link', 'categorias']

        # Define widgets personalizados para os campos, adicionando classes CSS e placeholders.
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o título'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite a descrição'}),
            'autor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Autor da notícia'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link da notícia'}),
            'categorias': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

        # Define rótulos personalizados para os campos exibidos no formulário.
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'autor': 'Autor',
            'link': 'Link',
            'categorias': 'Categorias',
        }


class FiltroNoticiasForm(forms.Form):
    # Campos existentes
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        label="Categoria",
        empty_label="Todas as Categorias"
    )
    autor = forms.CharField(
        max_length=100,
        required=False,
        label="Autor",
        widget=forms.TextInput(attrs={'placeholder': 'Autor'})
    )
    ordenacao = forms.ChoiceField(
        choices=[
            ('mais_novo', 'Mais Novo Primeiro'),
            ('mais_velho', 'Mais Velho Primeiro')
        ],
        required=False,
        label="Ordenar Por"
    )

    # Novo campo de busca
    busca = forms.CharField(
        max_length=255,
        required=False,
        label="Buscar Notícia",
        widget=forms.TextInput(attrs={'placeholder': 'Digite o título...'})
    )
