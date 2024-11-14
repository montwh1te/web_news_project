from django.shortcuts import render, get_object_or_404
from .models import Categoria, Noticias
from django.utils.text import slugify
from django.http import JsonResponse



def home(request):
    ultima_noticia = Noticias.objects.all().order_by('-id').first()
    outras_noticias = Noticias.objects.all().order_by('-data_publicacao')[1:5]  # Outras notícias

    # Excluir as notícias que já estão no banner principal e nas outras notícias destacadas
    ids_excluidos = [ultima_noticia.id] if ultima_noticia else []
    ids_excluidos += [noticia.id for noticia in outras_noticias]
    todas_as_noticias = Noticias.objects.exclude(id__in=ids_excluidos).order_by('-data_publicacao')

    categorias = Categoria.objects.all()
    categorias = Categoria.objects.exclude(nome_categoria='Outros')


    # Verificando se a última notícia e outras notícias possuem slug
    if ultima_noticia and not ultima_noticia.slug:
        ultima_noticia.slug = slugify(ultima_noticia.titulo)
        ultima_noticia.save()

    return render(request, 'html/index.html', {
        'ultima_noticia': ultima_noticia,
        'outras_noticias': outras_noticias,
        'todas_as_noticias': todas_as_noticias,  # Incluindo todas as outras notícias
        'categorias': categorias
    })


def detalhes_noticia(request, slug):
    noticia = get_object_or_404(Noticias, slug=slug)
    
    # Obtém a primeira categoria e define uma cor para ela
    categoria = noticia.categorias.first()
    categoria_nome = categoria.nome_categoria if categoria else "Outros"
    
    cores_times = {
        "atletico_mg": "#000000",         
        "atletico_pr": "#cc0000",          
        "bahia": "#0033cc",              
        "botafogo": "#000000",            
        "bragantino": "#cc0000",          
        "corinthians": "#333333",          
        "cruzeiro": "#003399",            
        "cuiaba": "#009933",              
        "flamengo": "#ff0000",             
        "fluminense": "#990000",        
        "fortaleza": "#003399",            
        "goias": "#009933",               
        "gremio": "#0066cc",             
        "internacional": "#cc0000",        
        "palmeiras": "#006633",           
        "santos": "#000000",            
        "sao_paulo": "#cc0000",         
        "vasco": "#000000",               
        "coritiba": "#009933",             
        "america_mg": "#009933",           
        "selecao": "#ffcc00"
    }
    
    cor_categoria = cores_times.get(categoria_nome.lower(), "#cccccc")  # usa a cor padrão se não encontrado

    # Gerar o nome do template com base no slug
    template_name = f'html/noticias/{noticia.slug}.html'
    
    return render(request, template_name, {
        'noticia': noticia, 
        'categoria_nome': categoria_nome,
        'cor_categoria': cor_categoria,
    })


def buscar_noticias(request):
    query = request.GET.get('q', '')
    if query:
        noticias = Noticias.objects.filter(descricao__icontains=query)
        results = []

        for noticia in noticias:
            results.append({
                'titulo': noticia.descricao,
                'slug': noticia.slug,
                'imagem_url': noticia.imagem_url,  # Chama a função imagem_url para pegar o caminho da imagem
            })

        return JsonResponse({'results': results})
    else:
        return JsonResponse({'results': []})
    


def exibir_categoria(request, nome_time):
    # Obtém a categoria correspondente ao nome do time ou exibe 404 se não existir
    categoria = get_object_or_404(Categoria, nome_categoria=nome_time)

    # Filtra as notícias relacionadas à categoria usando 'categorias' em vez de 'categoria'
    noticias = Noticias.objects.filter(categorias=categoria)

    # Define o template dinâmico para a página de categoria
    template_name = f'html/categorias/index_{nome_time}.html'

    context = {
        'main_title': nome_time.capitalize(),
        'cor_categoria': getattr(categoria, 'cor_categoria', "#cccccc"),  # Define cor padrão caso não exista `cor_categoria`
        'noticias': noticias,
    }

    return render(request, template_name, context)