# BIBLIOTECAS PADRÃO**
import json  
    # Para manipulação de objetos JSON (decodificação e codificação de dados).



# **BIBLIOTECAS DE TERCEIROS**
import requests  
    # Para fazer requisições HTTP a APIs externas.



# **IMPORTAÇÕES DO DJANGO**
from django.contrib.auth.decorators import login_required  
    # Para restringir acesso a usuários autenticados.
from django.shortcuts import render, get_object_or_404, redirect  
    # Funções para renderizar templates e redirecionar.
from django.http import JsonResponse  
    # Para enviar respostas JSON em requisições Ajax.
from django.utils.text import slugify  
    # Para gerar slugs a partir de strings.
from django.core.cache import cache 
    # Para armazenar e recuperar dados em cache.




# **IMPORTAÇÕES DE MÓDULOS INTERNOS**
from .models import Categoria, Noticias, InteracaoUsuario, Comentario  
    # Importa os modelos definidos na aplicação para interagir com o banco de dados.
from .utils import obter_tabela_brasileirao, obter_proximos_jogos     
    # Importa duas funções, uma utilitária personalizada para obter a tabela do Brasileirão e outra para os próximos jogos do Brasileirão.





# **FUNÇÃO DO INDEX.HTML**
def home(request):
    ultima_noticia = Noticias.objects.all().order_by('-id').first()
        # Obtém a última notícia publicada, ordenando pelo id em ordem decrescente.
    outras_noticias = Noticias.objects.all().order_by('-id')[1:5]
        # Obtém as próximas quatro notícias publicadas, excluindo a última.


    # **Cria uma lista de IDs das notícias já selecionadas.**
    ids_excluidos = [ultima_noticia.id] if ultima_noticia else []  
        # Se `ultima_noticia` não for `None`, adiciona o ID da última notícia à lista `ids_excluidos`.
        # Caso contrário, a lista será vazia ([]).
    ids_excluidos += [noticia.id for noticia in outras_noticias]  
        # Adiciona os IDs de todas as notícias em `outras_noticias` à lista `ids_excluidos`.

    
    todas_as_noticias = Noticias.objects.exclude(id__in=ids_excluidos).order_by('-data_publicacao')
        # Obtém todas as notícias restantes, excluindo os IDs acima.
    categorias = Categoria.objects.exclude(nome_categoria='Outros')
        # Obtém todas as categorias, excluindo a categoria "Outros".

 
    if ultima_noticia and not ultima_noticia.slug:
        # Verifica se existe uma última notícia e se ela ainda não tem um slug.
        ultima_noticia.slug = slugify(ultima_noticia.titulo)
            # Gera o slug a partir do título da notícia usando a função `slugify`.
        ultima_noticia.save()
            # Salva a notícia com o slug gerado no banco de dados.

    
    tabela = cache.get('tabela_brasileirao')
        # Busca a tabela do Brasileirão no cache.
    if not tabela:
        try:
            
            tabela = obter_tabela_brasileirao()
                # Caso não exista no cache, busca a tabela usando uma função externa.
            cache.set('tabela_brasileirao', tabela, timeout=60 * 60)
                # Armazena a tabela no cache por 1 hora.
        except Exception as e:
            tabela = []
                # Em caso de erro, define a tabela como uma lista vazia.

    
    proximos_jogos = cache.get('proximos_jogos')
        # Busca os próximos jogos no cache.
    if not proximos_jogos:
        proximos_jogos = obter_proximos_jogos()
            # Caso não exista no cache, obtém os próximos jogos da API.
        cache.set('proximos_jogos', proximos_jogos, timeout=60 * 60)
            # Armazena os próximos jogos no cache por 1 hora.


    # **Renderiza a página inicial com os dados obtidos.**
    return render(request, 'html/index.html', {
        'ultima_noticia': ultima_noticia,  
            # Última notícia.
        'outras_noticias': outras_noticias,  
            # Outras quatro notícias.
        'todas_as_noticias': todas_as_noticias,  
            # Restante das notícias.
        'categorias': categorias,  
            # Categorias disponíveis.
        'tabela': tabela,  
            # Tabela do Brasileirão.
        'proximos_jogos': proximos_jogos,  
            # Próximos jogos.
    })





# **FUNÇÃO DA BARRA DE PESQUISA**
def buscar_noticias(request):
    query = request.GET.get('q', '')  
        # Obtém a string de busca a partir da URL.


    if query:
        

        noticias = Noticias.objects.filter(descricao__icontains=query)
            # Busca notícias cuja descrição contenha a string de busca (case-insensitive).
            # Case-insensitive significa que a busca não faz distinção entre letras maiúsculas e minúsculas.
        results = []  
            # Inicializa uma lista para armazenar os resultados.


        for noticia in noticias:
            # Adiciona os dados relevantes de cada notícia à lista de resultados.
            results.append({
                'titulo': noticia.descricao,  
                    # Descrição da notícia.
                'slug': noticia.slug,  
                    # Slug da notícia para redirecionamento.
                'imagem_url': noticia.imagem_url,  
                    # URL da imagem da notícia.
            })

        
        return JsonResponse({'results': results})
            # Retorna os resultados em formato JSON.
            # converte para JSON usando JsonResponse, que é uma forma de retornar dados estruturados para o front-end.
    else:
        return JsonResponse({'results': []})
            # Retorna uma lista vazia se nenhum termo de busca for fornecido





# **FUNÇÃO DO MODELO.HTML**
# **FUNÇÃO DA PÁGINA DE CADA NOTÍCIA**
def detalhes_noticia(request, slug):
    noticia = get_object_or_404(Noticias, slug=slug)    
        # Obtém uma notícia específica com base no slug ou retorna erro 404.


    categoria = noticia.categorias.first()
        # Obtém a primeira categoria associada à notícia.
    categoria_nome = categoria.nome_categoria if categoria else "Outros"
        # Define o nome da categoria, ou "Outros" se nenhuma for encontrada.

    
    todas_as_noticias = Noticias.objects.all().order_by('-data_publicacao')
        # Obtém todas as notícias, ordenadas por data de publicação.
    noticias_agrupadas = [
        todas_as_noticias[i:i + 3] for i in range(0, len(todas_as_noticias), 3)
            # Agrupa as notícias em grupos de três para exibição.
    ]
    
    cores_times = {
        "atletico_mg": "#000000",      
        "atletico_pr": "#D81E05",      
        "bahia": "#003DA5",             
        "botafogo": "#000000",         
        "bragantino": "#FF0000",        
        "corinthians": "#000000",       
        "cruzeiro": "#003087",         
        "cuiaba": "#009739",           
        "flamengo": "#A61B20",         
        "fluminense": "#006847",       
        "fortaleza": "#002D72",        
        "goias": "#008C45",            
        "gremio": "#00AEEF",            
        "internacional": "#D6001C",     
        "palmeiras": "#1E7A34",         
        "santos": "#000000",           
        "sao_paulo": "#DD0032",         
        "vasco": "#000000",             
        "coritiba": "#006847",          
        "america_mg": "#006847",        
        "selecao": "#FFCC29"            
    }
        #Seleceiona a cor dos times para a pagina index_nomedotime.html
    
    cor_categoria = cores_times.get(categoria_nome.lower(), "#cccccc")

    template_name = f'html/noticias/{noticia.slug}.html'
        # Define o nome do template com base no slug da notícia.


    comentarios = Comentario.objects.filter(noticia=noticia).order_by('-data_criacao')
        # Obtém os comentários associados à notícia, ordenados por data de criação.


    # Renderiza a página de detalhes da notícia com os dados fornecidos.
    return render(request, template_name, {
        'noticia': noticia,  
            # Dados da notícia.
        'categoria_nome': categoria_nome, 
            # Nome da categoria.
        'noticias_agrupadas': noticias_agrupadas,  
            # Notícias agrupadas para exibição.
        'comentarios': comentarios,  
            # Comentários da notícia.
        'cor_categoria': cor_categoria
            #cor da categoria.
    })




# **FUNÇÃO DO MODELO.HTML**
# **FUNÇÃO DO LIKE**
@login_required
def atualizar_like(request, slug):
    if request.method == 'POST':
        
        noticia = get_object_or_404(Noticias, slug=slug)
            # Obtém a notícia associada ao slug ou retorna erro 404.
        
        usuario = request.user
            # Obtém o usuário autenticado.
        
        interacao, created = InteracaoUsuario.objects.get_or_create(
            noticia=noticia,
            usuario=usuario
        )   # Busca ou cria uma interação do usuário com a notícia.

       
        interacao.like = not interacao.like
            # Alterna o estado do like (curtido ou não curtido).
        interacao.save()

        
        noticia.like_count = InteracaoUsuario.objects.filter(noticia=noticia, like=True).count()
            # Recalcula o número total de likes na notícia.
        noticia.save()

        # Retorna os dados do like em formato JSON.
        return JsonResponse({
            'like_count': noticia.like_count,  
                # Número total de likes.
            'liked': interacao.like  
                # Status do like (True/False).
        })
    return JsonResponse({'error': 'Método inválido'}, status=400)
        # Retorna erro 400 para métodos não suportados.




# **FUNÇÃO DO MODELO.HTML**
# **FUNÇÃO DO COMENTÁRIO**
@login_required
def adicionar_comentario(request, slug):
    noticia = get_object_or_404(Noticias, slug=slug)
        # Busca uma notícia pelo slug ou retorna um erro 404 caso não seja encontrada.


    if request.method == 'POST':  
        # Garante que a requisição é do tipo POST.
        try:
            # Decodifica o corpo da requisição (JSON) enviado pelo frontend.
            data = json.loads(request.body)
            comentario_texto = data.get('comentario')  
                # Obtém o texto do comentário do JSON.
        except json.JSONDecodeError:
            # Retorna um erro JSON se os dados enviados forem inválidos.
            return JsonResponse({'success': False, 'error': 'Dados inválidos enviados.'}, status=400)

        if comentario_texto:
            # Cria um novo comentário associado à notícia e ao usuário.
            Comentario.objects.create(
                usuario=request.user,
                noticia=noticia,
                comentario=comentario_texto
            )
                # Retorna uma resposta JSON confirmando o sucesso e os dados do comentário.
            return JsonResponse({
                'success': True,
                'username': request.user.username,
                'comment': comentario_texto,
            })
       
        return JsonResponse({'success': False, 'error': 'Comentário vazio.'}, status=400)
            # Retorna um erro JSON se o comentário estiver vazio.

    
    return JsonResponse({'success': False, 'error': 'Método inválido.'}, status=400)
        # Retorna um erro JSON se o método da requisição for inválido.




# **FUNÇÃO DO MODELO_CATEGORIA.HTML**
# **FUNÇÃO DOS PRÓXIMOS JOGOS DA CATEGORIA EXPECIFICA**
def buscar_proximos_jogos(time_id):
    # Define a URL da API para buscar os próximos jogos de um time específico.
    api_url = f"https://api.futebol.com/v1/fixtures?team_id={time_id}&status=scheduled"
    
    # Define os cabeçalhos da requisição, incluindo o token de autenticação.
    headers = {"Authorization": "Bearer live_2a8fa6e7d603888fb9656c01ac3240"}

    # Envia a requisição para a API.
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:  # Verifica se a requisição foi bem-sucedida.
        return response.json()  # Retorna os dados JSON com os próximos jogos.
    else:
        return []  # Retorna uma lista vazia em caso de erro.




# **FUNÇÃO DO INDEX.HTML**
# **FUNÇÃO DOS ÍCONES DOS TIMES, PARA A PAGINA DE CADA TIME**
def exibir_categoria(request, nome_time):
    # Busca a categoria pelo nome do time ou retorna erro 404.
    categoria = get_object_or_404(Categoria, nome_categoria=nome_time)

    # Filtra as notícias relacionadas à categoria, ordenadas por ID (mais recentes primeiro).
    noticias = Noticias.objects.filter(categorias=categoria).order_by('-id')

    # Obtém a última notícia publicada (mais recente).
    ultima_noticia = noticias.first()

    # Obtém as próximas três notícias mais recentes, excluindo a última.
    ultimas_tres_noticias = noticias[1:4]

    # Obtém as notícias restantes, excluindo as quatro primeiras.
    restantes_noticias = noticias[4:]

    # Define o template dinâmico para exibir a categoria.
    template_name = f'html/categorias/index_{nome_time}.html'

    # Define o contexto para renderizar o template.
    context = {
        'main_title': nome_time,  # Nome do time como título principal.
        'cor_categoria': getattr(categoria, 'cor_categoria', "#3333"),  # Cor associada à categoria (padrão se não definido).
        'noticias': restantes_noticias,  # Notícias restantes.
        'ultima_noticia': ultima_noticia,  # Última notícia publicada.
        'ultimas_tres_noticias': ultimas_tres_noticias,  # Próximas três notícias mais recentes.
    }

    # Renderiza a página da categoria com o contexto fornecido.
    return render(request, template_name, context)










