import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Noticias, InteracaoUsuario
from django.utils.text import slugify
from django.http import JsonResponse
from .utils import obter_tabela_brasileirao
from django.core.cache import cache
from django.conf import settings
from .forms import ComentarioForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def obter_proximos_jogos():
    # Definindo a URL da API onde os dados dos próximos jogos serão obtidos.
    url = "https://api.api-futebol.com.br/v1/campeonatos/10/rodadas/34"  # Substitua '34' pela rodada desejada dinamicamente, se necessário
    
    # Definindo os cabeçalhos da requisição, incluindo o token de autenticação para acessar a API.
    headers = {
        "Authorization": f"Bearer {settings.API_FUTEBOL_KEY}"  # Insira seu token da API aqui
    }

    try:
        # Enviando a requisição HTTP para obter os dados da API.
        response = requests.get(url, headers=headers)
        # Verificando se a resposta da requisição foi bem-sucedida. Caso contrário, lança uma exceção.
        response.raise_for_status()
        # Retornando os dados JSON da resposta, especificamente a lista de partidas (proximos jogos).
        return response.json().get('partidas', [])
    except requests.exceptions.RequestException as e:
        # Caso ocorra qualquer erro durante a requisição, imprime o erro e retorna uma lista vazia.
        print(f"Erro ao buscar próximos jogos: {e}")
        return []


def home(request):
    # Buscando a última notícia da base de dados, ordenada pela data de publicação (id crescente).
    ultima_noticia = Noticias.objects.all().order_by('-data_publicacao').first()
    # Buscando as 4 notícias seguintes, ordenadas pela data de publicação.
    outras_noticias = Noticias.objects.all().order_by('-data_publicacao')[1:5]

    # Excluindo as notícias que já foram buscadas (última notícia e as outras notícias).
    ids_excluidos = [ultima_noticia.id] if ultima_noticia else []  # Lista contendo o ID da última notícia, se existir.
    ids_excluidos += [noticia.id for noticia in outras_noticias]  # Adicionando os IDs das outras notícias a serem excluídas.
    # Buscando todas as notícias restantes, exceto as já excluídas, e ordenando por data de publicação.
    todas_as_noticias = Noticias.objects.exclude(id__in=ids_excluidos).order_by('-data_publicacao')

    # Buscando todas as categorias, exceto a categoria 'Outros'.
    categorias = Categoria.objects.exclude(nome_categoria='Outros')
    

    # Garantindo que a última notícia tenha um slug, caso não tenha, gerando e salvando um.
    if ultima_noticia and not ultima_noticia.slug:
        ultima_noticia.slug = slugify(ultima_noticia.titulo)  # Criando um slug baseado no título da notícia.
        ultima_noticia.save()  # Salvando a última notícia com o novo slug.

    # Buscando os dados da tabela do Brasileirão armazenados no cache (caso já exista).
    tabela = cache.get('tabela_brasileirao')
    if not tabela:
        try:
            # Caso não exista cache para a tabela, obtendo a tabela do Brasileirão por meio de uma função externa.
            tabela = obter_tabela_brasileirao()  # Presumindo que você já tenha esta função definida.
            # Armazenando os dados da tabela no cache por 1 hora (60 * 60 segundos).
            cache.set('tabela_brasileirao', tabela, timeout=60 * 60)
        except Exception as e:
            tabela = []  # Em caso de erro, definindo a tabela como uma lista vazia.

    # Buscando os próximos jogos armazenados no cache.
    proximos_jogos = cache.get('proximos_jogos')
    if not proximos_jogos:
        # Caso não exista cache para os próximos jogos, obtendo os dados da API.
        proximos_jogos = obter_proximos_jogos()
        # Armazenando os próximos jogos no cache por 1 hora (60 * 60 segundos).
        cache.set('proximos_jogos', proximos_jogos, timeout=60 * 60)

    # Retornando a renderização da página inicial (index.html) com os dados buscados.
    return render(request, 'html/index.html', {
        'ultima_noticia': ultima_noticia,  # Passando a última notícia para o template.
        'outras_noticias': outras_noticias,  # Passando as outras notícias para o template.
        'todas_as_noticias': todas_as_noticias,  # Passando todas as notícias restantes para o template.
        'categorias': categorias,  # Passando as categorias para o template.
        'tabela': tabela,  # Passando a tabela do Brasileirão para o template.
        'proximos_jogos': proximos_jogos,  # Passando os próximos jogos para o template.
    })



def detalhes_noticia(request, slug):
    noticia = get_object_or_404(Noticias, slug=slug)
    
    # Obtém a primeira categoria e define uma cor para ela
    categoria = noticia.categorias.first()
    categoria_nome = categoria.nome_categoria if categoria else "Outros"
    
  
    cores_times = {
       "atletico_mg": "#000000",       # Preto
        "atletico_pr": "#D81E05",       # Vermelho
        "bahia": "#003DA5",             # Azul
        "botafogo": "#000000",          # Preto
        "bragantino": "#FF0000",        # Vermelho
        "corinthians": "#000000",       # Preto
        "cruzeiro": "#003087",          # Azul
        "cuiaba": "#009739",            # Verde
        "flamengo": "#A61B20",          # Vermelho
        "fluminense": "#006847",        # Verde
        "fortaleza": "#002D72",         # Azul
        "goias": "#008C45",             # Verde
        "gremio": "#00AEEF",            # Azul Celeste
        "internacional": "#D6001C",     # Vermelho
        "palmeiras": "#1E7A34",         # Verde
        "santos": "#000000",            # Preto
        "sao_paulo": "#DD0032",         # Vermelho
        "vasco": "#000000",             # Preto
        "coritiba": "#006847",          # Verde
        "america_mg": "#006847",        # Verde
        "selecao": "#FFCC29"  
    }
    noticia = get_object_or_404(Noticias, slug=slug)

    todas_as_noticias = Noticias.objects.all().order_by('-data_publicacao')

    cor_categoria = cores_times.get(categoria_nome.lower(), "#cccccc")  # usa a cor padrão se não encontrado


  

    noticias_agrupadas = [
        todas_as_noticias[i:i+3] for i in range(0, len(todas_as_noticias), 3)
    ]

    # Gerar o nome do template com base no slug
    template_name = f'html/noticias/{noticia.slug}.html'

    comentarios = InteracaoUsuario.objects.filter(noticia=noticia).order_by('-id')

    return render(request, template_name, {
        'noticia': noticia, 
        'categoria_nome': categoria_nome,
        'cor_categoria': cor_categoria,
        'noticias_agrupadas': noticias_agrupadas,
        'comentarios': comentarios,
        
    })
@login_required
def atualizar_like(request, slug):
    if request.method == 'POST':
        # Obtém a notícia e o usuário
        noticia = get_object_or_404(Noticias, slug=slug)
        usuario = request.user

        # Busca ou cria a interação
        interacao, created = InteracaoUsuario.objects.get_or_create(
            noticia=noticia,
            usuario=usuario
        )

        # Alterna o estado do like
        interacao.like = not interacao.like
        interacao.save()

        # Recalcula o contador de likes
        noticia.like_count = InteracaoUsuario.objects.filter(noticia=noticia, like=True).count()
        noticia.save()

        return JsonResponse({
            'like_count': noticia.like_count,
            'liked': interacao.like
        })

    return JsonResponse({'error': 'Método inválido'}, status=400)



@login_required
def salvar_comentario(request, noticia_id):
    noticia = get_object_or_404(Noticias, id=noticia_id)
    if request.method == 'POST':
        comentario_texto = request.POST.get('comentario')
        if comentario_texto:
            # Busca ou cria a interação
            interacao, created = InteracaoUsuario.objects.get_or_create(
                noticia=noticia,
                usuario=request.user
            )

            # Atualiza o comentário
            interacao.comentario = comentario_texto
            interacao.save()

        return redirect('detalhes_noticia', slug=noticia.slug)

    return JsonResponse({'error': 'Método inválido'}, status=400)







@login_required
def adicionar_comentario(request, slug):
    noticia = get_object_or_404(Noticias, slug=slug)

    if request.method == 'POST':
        comentario_texto = request.POST.get('comentario')
        if comentario_texto:  # Garante que não há comentários vazios
            InteracaoUsuario.objects.create(
                usuario=request.user,
                noticia=noticia,
                comentario=comentario_texto
            )
        return redirect('detalhes_noticia', slug=slug)

    return JsonResponse({'error': 'Método inválido'}, status=400)


@login_required

def interagir(request, slug):
    noticia = get_object_or_404(Noticias, slug=slug)
    usuario = request.user

    if request.method == 'POST':
        # Para comentários
        if 'comentario' in request.POST:
            comentario = request.POST.get('comentario')
            InteracaoUsuario.objects.create(
                usuario=usuario,
                noticia=noticia,
                comentario=comentario
            )
        # Para likes
        if 'like' in request.POST:
            interacao, created = InteracaoUsuario.objects.get_or_create(
                usuario=usuario,
                noticia=noticia
            )
            interacao.like = not interacao.like
            interacao.save()

            # Atualizar contagem de likes
            noticia.like_count = InteracaoUsuario.objects.filter(noticia=noticia, like=True).count()
            noticia.save()

    return redirect('detalhes_noticia', slug=noticia.slug)





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



