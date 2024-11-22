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
from .models import Categoria, Noticias, InteracaoUsuario, Comentario, CategoriaNoticias
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


    
    categorias_serie_a = Categoria.objects.all().filter(serie='A')
    categorias_serie_b = Categoria.objects.all().filter(serie='B')

    for jogo in proximos_jogos:
        if jogo["placar"]:  # Verifica se há placar disponível
            import re  # Biblioteca para expressões regulares

            # Encontra os números no placar
            numeros = re.findall(r'\d+', jogo["placar"])

            if len(numeros) == 2:  # Verifica se encontrou dois números
                jogo["placar_numerico"] = f"{numeros[0]} x {numeros[1]}"
            else:
                jogo["placar_numerico"] = None  # Placar inválido
        else:
            jogo["placar_numerico"] = None


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
        'categorias_serie_a': categorias_serie_a,

        'categorias_serie_b':categorias_serie_b,
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

    categoria_cor = categoria.cor 
    print(categoria.cor) 


    categoria_nome = categoria.nome_categoria if categoria else "Outros"
        # Define o nome da categoria, ou "Outros" se nenhuma for encontrada.

    
    todas_as_noticias = Noticias.objects.all().order_by('-data_publicacao')
        # Obtém todas as notícias, ordenadas por data de publicação.
    noticias_agrupadas = [
        todas_as_noticias[i:i + 3] for i in range(0, len(todas_as_noticias), 3)
            # Agrupa as notícias em grupos de três para exibição.
    ]
    
    
    

    template_name = f'html/noticias/{noticia.slug}.html'
        # Define o nome do template com base no slug da notícia.

    usuario_curtiu = False
    if request.user.is_authenticated:
        usuario_curtiu = InteracaoUsuario.objects.filter(
            noticia=noticia, 
            usuario=request.user, 
            like=True
        ).exists()

    comentarios = Comentario.objects.filter(noticia=noticia).order_by('-data_criacao')
        # Obtém os comentários associados à notícia, ordenados por data de criação.

    


    # Renderiza a página de detalhes da notícia com os dados fornecidos.
    return render(request, template_name, {
        'noticia': noticia,  
        'categoria_nome': categoria_nome, 
        'noticias_agrupadas': noticias_agrupadas,  
        'comentarios': comentarios,  
        'usuario_curtiu': usuario_curtiu,  
        'categoria_cor': categoria_cor,  # Remova o espaço extra no nome
    })






# **FUNÇÃO DO MODELO.HTML**
# **FUNÇÃO DO LIKE**
@login_required  
# Garante que apenas usuários autenticados possam acessar esta view.
def atualizar_like(request, slug):
    if request.method == 'POST':  
        # Verifica se a requisição é do tipo POST, pois apenas este tipo de requisição é permitido para esta ação.
        noticia = get_object_or_404(Noticias, slug=slug)  
            # Obtém a instância de 'Noticias' com base no slug ou retorna um erro 404 se não encontrado.
        usuario = request.user  
            # Obtém o usuário autenticado que fez a requisição.

        # Tenta recuperar uma interação do usuário com a notícia ou cria uma nova se não existir.
        interacao, created = InteracaoUsuario.objects.get_or_create(
            noticia=noticia,
            usuario=usuario
        )
        interacao.like = not interacao.like  
            # Inverte o estado do like: se era True passa para False, e vice-versa.
        interacao.save()  
            # Salva a interação no banco de dados.

        # Atualiza a contagem de likes da notícia com base nas interações de usuários onde 'like=True'.
        noticia.like_count = InteracaoUsuario.objects.filter(noticia=noticia, like=True).count()
        noticia.save()  
            # Salva a contagem de likes atualizada na instância da notícia.

        # Retorna uma resposta JSON contendo a nova contagem de likes e o estado atual do like do usuário.
        return JsonResponse({
            'like_count': noticia.like_count,
            'liked': interacao.like
        })
    return JsonResponse({'error': 'Método inválido'}, status=400)  
        # Retorna um erro JSON se a requisição não for do tipo POST.






# **FUNÇÃO DO MODELO.HTML**
# **FUNÇÃO DO COMENTÁRIO**
@login_required
# Decorador que exige que o usuário esteja autenticado para acessar esta função.
def adicionar_comentario(request, slug):
    # Função para adicionar um comentário a uma notícia específica.

    if request.method == 'POST':
        # Verifica se a requisição recebida é do tipo POST.

        noticia = get_object_or_404(Noticias, slug=slug)
            # Busca a notícia no banco de dados com base no slug fornecido.
            # Retorna um erro 404 se a notícia não for encontrada.

        try:
            data = json.loads(request.body)
                # Tenta carregar os dados enviados no corpo da requisição como JSON.

            comentario_texto = data.get('comentario')
                # Obtém o texto do comentário enviado pelo cliente.

        except json.JSONDecodeError:
            # Captura erros de decodificação JSON, caso os dados enviados estejam em um formato inválido.

            return JsonResponse({'success': False, 'error': 'Dados inválidos enviados.'}, status=400)
                # Retorna uma resposta JSON indicando que houve erro no envio dos dados.

        if comentario_texto:
            # Verifica se o texto do comentário não está vazio.

            comentario = Comentario.objects.create(
                usuario=request.user,
                    # Associa o comentário ao usuário atualmente logado.

                noticia=noticia,
                    # Relaciona o comentário à notícia específica.

                comentario=comentario_texto
                    # Salva o texto do comentário.
            )

            return JsonResponse({
                'success': True,
                    # Indica que o comentário foi salvo com sucesso.
                'username': request.user.username,
                    # Retorna o nome de usuário do autor do comentário.
                'comment': comentario.comentario,
                    # Retorna o texto do comentário.
                'foto': request.user.foto.url if request.user.foto else '/static/images/default-avatar.png'
                    # Retorna o caminho para a foto do usuário, ou uma imagem padrão caso o usuário não tenha uma foto.
            })

        return JsonResponse({'success': False, 'error': 'Comentário vazio.'}, status=400)
        # Retorna um erro JSON caso o campo de comentário esteja vazio.
    return JsonResponse({'success': False, 'error': 'Método inválido.'}, status=400)
    # Retorna um erro JSON caso a requisição não seja do tipo POST.





# **FUNÇÃO DO MODELO_CATEGORIA.HTML**
# **FUNÇÃO DOS PRÓXIMOS JOGOS DA CATEGORIA ESPECÍFICA**
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

    categoria_cor = categoria.cor 
    print(categoria.cor) 

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
        'categoria_cor': categoria_cor,
    }

    # Renderiza a página da categoria com o contexto fornecido.
    return render(request, template_name, context)










