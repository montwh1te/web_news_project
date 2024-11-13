from django.shortcuts import render, get_object_or_404
from .models import Noticias
from django.utils.text import slugify

def home(request):
    ultima_noticia = Noticias.objects.all().order_by('-id').first()
    outras_noticias = Noticias.objects.all().order_by('-data_publicacao')[1:5]  # Outras notícias

    # Excluir as notícias que já estão no banner principal e nas outras notícias destacadas
    ids_excluidos = [ultima_noticia.id] if ultima_noticia else []
    ids_excluidos += [noticia.id for noticia in outras_noticias]
    todas_as_noticias = Noticias.objects.exclude(id__in=ids_excluidos).order_by('-data_publicacao')

    # Verificando se a última notícia e outras notícias possuem slug
    if ultima_noticia and not ultima_noticia.slug:
        ultima_noticia.slug = slugify(ultima_noticia.titulo)
        ultima_noticia.save()

    return render(request, 'html/index.html', {
        'ultima_noticia': ultima_noticia,
        'outras_noticias': outras_noticias,
        'todas_as_noticias': todas_as_noticias  # Incluindo todas as outras notícias
    })


def detalhes_noticia(request, slug):
    noticia = get_object_or_404(Noticias, slug=slug)
    
    # Gerar o nome do template com base no slug
    template_name = f'html/noticias/{noticia.slug}.html'
    
    return render(request, template_name, {'noticia': noticia})