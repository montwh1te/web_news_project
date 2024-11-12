from django.shortcuts import render, get_object_or_404
from .models import Noticias
from django.utils.text import slugify


def home(request):
    ultima_noticia = Noticias.objects.all().order_by('-id').first()
    outras_noticias = Noticias.objects.all().order_by('-data_publicacao')[1:5]  # Outras notícias
    
    # Verificando se a última notícia e outras notícias possuem slug
    if ultima_noticia and not ultima_noticia.slug:
        ultima_noticia.slug = slugify(ultima_noticia.titulo)
        ultima_noticia.save()

    return render(request, 'html/index.html', {'ultima_noticia': ultima_noticia, 'outras_noticias': outras_noticias})


def detalhes_noticia(request, slug):
    noticia = get_object_or_404(Noticias, slug=slug)
    
    # Gerar o nome do template com base no slug
    template_name = f'html/noticias/{noticia.slug}.html'
    
    return render(request, template_name, {'noticia': noticia})