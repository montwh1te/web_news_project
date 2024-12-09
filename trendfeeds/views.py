''' **BIBLIOTECAS PADRÃO** '''
# Para manipulação de objetos JSON (decodificação e codificação de dados).
import json 

# Para trabalhar com expressões regulares, útil para encontrar padrões de texto.
import re  



''' **BIBLIOTECAS DE TERCEIROS** '''
# Para fazer requisições HTTP a APIs externas.
import requests  

# Para interagir com o sistema operacional, como manipulação de arquivos e caminhos.
import os  

# Para implementar um cache com tempo de expiração.
from cachetools import TTLCache  



''' **IMPORTAÇÕES DO DJANGO** '''
# Para restringir acesso a usuários autenticados.
from django.contrib.auth.decorators import login_required  

# Funções para renderizar templates, recuperar objetos do banco de dados ou redirecionar o usuário.
from django.shortcuts import render, get_object_or_404, redirect

# Para enviar respostas JSON em requisições Ajax.
from django.http import JsonResponse  

# Para gerar slugs a partir de strings.
from django.utils.text import slugify 

# Para armazenar e recuperar dados em cache.
from django.core.cache import cache  

# Para acessar as configurações globais do projeto, como chaves e parâmetros de banco de dados.
from django.conf import settings  

# Para exibir mensagens ao usuário, como erros ou confirmações.
from django.contrib import messages  

# Para obter o modelo de usuário personalizado ou padrão usado pelo sistema.
from django.contrib.auth import get_user_model  



''' **IMPORTAÇÕES DE MÓDULOS INTERNOS** '''
# Importa os modelos definidos na aplicação para interagir com o banco de dados.
from .models import Categoria, Noticias, InteracaoUsuario, Comentario, CategoriaNoticias  

# Importa duas funções utilitárias personalizadas, uma para obter a tabela do Brasileirão e outra para os próximos jogos.
from .utils import obter_tabela_brasileirao, obter_proximos_jogos, obter_jogos_um_time


# Importa o formulário personalizado para criação e edição de notícias.
from .forms import NoticiasForm  






''' Função que lida com a página inicial da aplicação. '''
def home(request):
    # Obtém a última notícia publicada, ordenando pelo id em ordem decrescente.
    ultima_noticia = Noticias.objects.all().order_by('-id').first()
    
    # Obtém as próximas quatro notícias publicadas, excluindo a última.
    outras_noticias = Noticias.objects.all().order_by('-id')[1:5]

    # Cria uma lista de IDs das notícias já selecionadas.
    ids_excluidos = [ultima_noticia.id] if ultima_noticia else []  
        # Se `ultima_noticia` não for `None`, adiciona o ID da última notícia à lista `ids_excluidos`. 
        # Caso contrário, a lista será vazia ([]).
    
    # Adiciona os IDs de todas as notícias em `outras_noticias` à lista `ids_excluidos`.
    ids_excluidos += [noticia.id for noticia in outras_noticias]  

    # Obtém todas as notícias restantes, excluindo os IDs acima.
    todas_as_noticias = Noticias.objects.exclude(id__in=ids_excluidos).order_by('-data_publicacao')

    # Obtém todas as categorias, excluindo a categoria "Outros".
    categorias = Categoria.objects.exclude(nome_categoria='Outros')

    # Verifica se existe uma última notícia e se ela ainda não tem um slug.
    if ultima_noticia and not ultima_noticia.slug:

        # Gera o slug a partir do título da notícia usando a função `slugify`.
        ultima_noticia.slug = slugify(ultima_noticia.titulo)

        # Salva a notícia com o slug gerado no banco de dados.
        ultima_noticia.save()

    # Busca a tabela do Brasileirão no cache.
    tabela = cache.get('tabela_brasileirao')

    # Caso não exista no cache, busca a tabela usando uma função externa.
    if not tabela:
        try:
            tabela = obter_tabela_brasileirao()

            # Caso a tabela não exista, tenta obter os dados da API externa.
            # Armazena a tabela no cache por 1 hora.
            cache.set('tabela_brasileirao', tabela, timeout=60 * 60)
        except Exception as e:

            # Em caso de erro, define a tabela como uma lista vazia.
            tabela = []

    # Busca os próximos jogos no cache.
    proximos_jogos = cache.get('proximos_jogos')

    # Caso não exista no cache, obtém os próximos jogos da API.
    if not proximos_jogos:
        proximos_jogos = obter_proximos_jogos()

        # Armazena os próximos jogos no cache por 1 hora.
        cache.set('proximos_jogos', proximos_jogos, timeout=60 * 60)

    # Obtém as categorias da série A e B do campeonato.
    categorias_serie_a = Categoria.objects.all().filter(serie='A')
    categorias_serie_b = Categoria.objects.all().filter(serie='B')

    # Verifica se há placar disponível para os jogos e formata os placares.
    for jogo in proximos_jogos:
        if jogo["placar"]:  

            # Verifica se há placar disponível para o jogo.
            # Biblioteca para expressões regulares para buscar números no placar.
            import re  

            # Encontra os números no placar.
            numeros = re.findall(r'\d+', jogo["placar"])

            # Verifica se encontrou dois números no placar.
            if len(numeros) == 2:  

                # Formata o placar como "número X número".
                jogo["placar_numerico"] = f"{numeros[0]}<span>X</span>{numeros[1]}"
            else:

                # Se o placar não for válido, define como None.
                jogo["placar_numerico"] = None
        else:

            # Caso não tenha placar, define como None.
            jogo["placar_numerico"] = None

    # Renderiza a página inicial com os dados obtidos.
    return render(request, 'html/index.html', {
        'ultima_noticia': ultima_noticia,  
        'outras_noticias': outras_noticias,  
        'todas_as_noticias': todas_as_noticias,  
        'categorias': categorias,  
        'tabela': tabela,  
        'proximos_jogos': proximos_jogos,  
        'categorias_serie_a': categorias_serie_a,
        'categorias_serie_b': categorias_serie_b,
    })





''' Função que lida com a busca de notícias através da barra de pesquisa. '''
def buscar_noticias(request):
    # Obtém a string de busca a partir da URL.
    query = request.GET.get('q', '')  

    # Verifica se há um termo de busca fornecido.
    if query:
        # Busca notícias cuja descrição contenha a string de busca (case-insensitive).
        noticias = Noticias.objects.filter(descricao__icontains=query)
            # Case-insensitive significa que a busca não faz distinção entre letras maiúsculas e minúsculas.
        
        # Inicializa uma lista para armazenar os resultados.
        results = []  

        # Itera sobre todas as notícias encontradas.
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

        # Retorna os resultados em formato JSON.
        # Converte os dados para JSON usando JsonResponse, que é uma forma de retornar dados estruturados para o front-end.
        return JsonResponse({'results': results})
    
    else:
        # Retorna uma lista vazia se nenhum termo de busca for fornecido.
        return JsonResponse({'results': []})





<<<<<<< HEAD
=======
''' Função que lida com a exibição da página de detalhes de uma notícia específica. '''
>>>>>>> 14d5c0173c95180a533e27988c634c59b03f33e1
def detalhes_noticia(request, slug):
    # Obtém uma notícia específica com base no slug ou retorna erro 404.
    noticia = get_object_or_404(Noticias, slug=slug)    

    # Obtém a primeira categoria associada à notícia.
    categoria = noticia.categorias.first()
    
    # Obtém a cor da categoria associada à notícia.
    categoria_cor = categoria.cor 
    print(categoria.cor)  # Imprime a cor da categoria para depuração.

    # Define o nome da categoria, ou "Outros" se nenhuma for encontrada.
    categoria_nome = categoria.nome_categoria if categoria else "Outros"
    categoria_nome_exibicao = categoria.nome if categoria else "Outros"


    # Cria uma lista de IDs das notícias já selecionadas.
    ids_excluidos = [noticia.id] if noticia else []  
<<<<<<< HEAD

    # Obtém todas as notícias que têm a mesma categoria da notícia atual, excluindo a própria notícia.
    noticias_com_mesma_categoria = Noticias.objects.filter(categorias=categoria).exclude(id__in=ids_excluidos).order_by('-data_publicacao')

    limite_noticias = noticias_com_mesma_categoria[:9]
    
    # Agrupa as notícias da mesma categoria em grupos de três para exibição.
    noticias_agrupadas = [
        limite_noticias[i:i + 3] for i in range(0, len(limite_noticias), 3)
    ]

    autor_parts = noticia.autor.split("—")
    autor_primeira_parte = autor_parts[0].strip()
    autor_segunda_parte = autor_parts[1].strip() if len(autor_parts) > 1 else ""

=======
    # Se `ultima_noticia` não for `None`, adiciona o ID da última notícia à lista `ids_excluidos`. 
    # Caso contrário, a lista será vazia ([]).
    
    
    # Obtém todas as notícias, ordenadas por data de publicação.
    todas_as_noticias = Noticias.objects.exclude(id__in=ids_excluidos).order_by('-data_publicacao')[1:11]
    
    # Agrupa as notícias em grupos de três para exibição.
    noticias_agrupadas = [
        todas_as_noticias[i:i + 3] for i in range(0, len(todas_as_noticias), 3)
    ]
   
   
>>>>>>> 14d5c0173c95180a533e27988c634c59b03f33e1

    # Define o nome do template com base no slug da notícia.
    template_name = f'html/noticias/{noticia.slug}.html'

    # Verifica se o usuário autenticado já curtiu a notícia.
    usuario_curtiu = False
    if request.user.is_authenticated:
        usuario_curtiu = InteracaoUsuario.objects.filter(
            noticia=noticia, 
            usuario=request.user, 
            like=True
        ).exists()

    # Obtém os comentários associados à notícia, ordenados por data de criação.
    comentarios = Comentario.objects.filter(noticia=noticia).order_by('-data_criacao')

<<<<<<< HEAD
    noticias_restantes = Noticias.objects.exclude(id__in=ids_excluidos).order_by('-data_publicacao')[9:]

=======
>>>>>>> 14d5c0173c95180a533e27988c634c59b03f33e1
    # Renderiza a página de detalhes da notícia com os dados fornecidos.
    return render(request, template_name, {
        'noticia': noticia,  
        'categoria_nome': categoria_nome, 
        'noticias_agrupadas': noticias_agrupadas,  
        'comentarios': comentarios,  
        'usuario_curtiu': usuario_curtiu,  
        'categoria_cor': categoria_cor, 
        'categoria_nome_exibicao': categoria_nome_exibicao,
<<<<<<< HEAD
        'autor_primeira_parte': autor_primeira_parte,
        'autor_segunda_parte': autor_segunda_parte,
        'noticias_restantes' : noticias_restantes,
=======
>>>>>>> 14d5c0173c95180a533e27988c634c59b03f33e1
    })





''' Função para atualizar o "like" de uma notícia. Somente usuários autenticados podem interagir. '''
@login_required
def atualizar_like(request, slug):
    # Verifica se a requisição é do tipo POST
    if request.method == 'POST':  
        noticia = get_object_or_404(Noticias, slug=slug)  # Obtém a notícia
        usuario = request.user  # Obtém o usuário

        # Tenta recuperar ou criar uma interação para o usuário com a notícia
        interacao, created = InteracaoUsuario.objects.get_or_create(
            noticia=noticia,
            usuario=usuario
        )

        # Inverte o estado do like
        interacao.like = not interacao.like  
        interacao.save()  # Salva a interação no banco de dados

        # Atualiza a contagem de likes da notícia
        noticia.like_count = InteracaoUsuario.objects.filter(noticia=noticia, like=True).count()
        noticia.save()  # Salva a contagem de likes atualizada

        # Retorna uma resposta JSON com a nova contagem de likes e o estado do like
        return JsonResponse({
            'like_count': noticia.like_count,
            'liked': interacao.like
        })

    return JsonResponse({'error': 'Método inválido'}, status=400)





''' Decorador que exige que o usuário esteja autenticado para acessar esta função. '''
@login_required
def adicionar_comentario(request, slug):
    if request.method == 'POST':
        noticia = get_object_or_404(Noticias, slug=slug)

        try:
            data = json.loads(request.body)
            comentario_texto = data.get('comentario')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Dados inválidos enviados.'}, status=400)

        if comentario_texto:
            comentario = Comentario.objects.create(
                usuario=request.user,
                noticia=noticia,
                comentario=comentario_texto
            )

            return JsonResponse({
                'success': True,
                'username': request.user.username,
                'comment': comentario.comentario,
                'foto': request.user.foto.url if request.user.foto else '/media/login.png'
            })

        return JsonResponse({'success': False, 'error': 'Comentário vazio.'}, status=400)

    return JsonResponse({'success': False, 'error': 'Método inválido.'}, status=400)





''' Define a URL da API para buscar os próximos jogos de um time específico. '''
def buscar_proximos_jogos(time_id):
    # Define a URL da API com o ID do time e o status "scheduled" para jogos agendados.
    api_url = f"https://api.futebol.com/v1/fixtures?team_id={time_id}&status=scheduled"
    
    # Define os cabeçalhos da requisição, incluindo o token de autenticação.
    headers = {"Authorization": "Bearer live_2a8fa6e7d603888fb9656c01ac3240"}

    # Envia a requisição para a API.
    response = requests.get(api_url, headers=headers)

    # Verifica se a requisição foi bem-sucedida (status code 200).
    if response.status_code == 200:

        # Retorna os dados JSON com os próximos jogos se a requisição for bem-sucedida.
        return response.json()
    else:

        # Retorna uma lista vazia em caso de erro na requisição.
        return []





''' Função que exibe a página de uma categoria específica (time), mostrando suas notícias. '''
def exibir_categoria(request, nome_time):
    """
    Exibe as informações da categoria de um time (nome do time).
    Obtém as últimas notícias e os próximos jogos do time.
    """
    # Busca a categoria pelo nome do time (verificando se existe)
    categoria = get_object_or_404(Categoria, nome_categoria=nome_time)

    # Obtém a cor associada à categoria
    categoria_cor = categoria.cor

    # Filtra as notícias relacionadas à categoria
    noticias = Noticias.objects.filter(categorias=categoria).order_by('-id')

    # Obtém a última notícia publicada
    ultima_noticia = noticias.first()

    # Obtém as próximas três notícias mais recentes, excluindo a última
    ultimas_tres_noticias = noticias[1:5]

    # Obtém as notícias restantes
    restantes_noticias = noticias[4:]

    # Define o template dinâmico com base no nome do time
    template_name = f'html/categorias/index_{nome_time}.html'

    # Define o contexto para renderizar o template
    context = {
        'main_title': nome_time,
        'cor_categoria': getattr(categoria, 'cor_categoria', "#3333"),
        'noticias': restantes_noticias,
        'ultima_noticia': ultima_noticia,
        'ultimas_tres_noticias': ultimas_tres_noticias,
        'categoria_cor': categoria_cor,
    }

    # Lista de rodadas a serem buscadas
    rodadas = [34, 35, 36, 37, 38,]  # Adicione aqui as rodadas desejadas

    # Obtemos os jogos do time a partir da função obter_jogos_um_time_multiplas_rodadas
    try:
        proximos_jogos = obter_jogos_um_time(nome_time, rodadas)
    except ValueError as e:
        # Caso o time não seja encontrado, você pode capturar o erro e tratá-lo (por exemplo, mostrando uma mensagem).
        return render(request, 'index.html', {'mensagem': str(e)})

    # Adiciona os próximos jogos ao contexto
    context['proximos_jogos'] = proximos_jogos

    # Renderiza o template com as informações doF time
    return render(request, template_name, context)





''' Função que exibe a página que mostra todas as noticias aos funcionários. '''
def pagina_noticias_funcionarios(request):
    # Obtém todas as notícias do banco de dados.
    noticias = Noticias.objects.all().order_by('-id')
    
    # Renderiza a página de funcionários com as notícias obtidas.
    # O contexto passado inclui todas as notícias para exibição na página.
    return render(request, 'html/todas_as_noticias_funcionarios.html', {'noticias': noticias})





''' Função que salva a notícia caso ela seja editada por um superuser. '''
def salvar_noticia_html(request, slug):
    # Verifica se o usuário é um administrador, caso contrário retorna erro 403 (Acesso negado)
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Acesso negado. Apenas administradores podem salvar notícias.'}, status=403)

    if request.method == 'POST':  
        # Verifica se o método da requisição é POST (usado para enviar dados ao servidor)
        try:
            # Obtém os dados recebidos do formulário
            titulo = request.POST.get('titulo', '').strip()  # Título da notícia
            conteudo = request.POST.get('conteudo', '').strip()  # Conteúdo da notícia
            imagens_alteradas = request.FILES  # Imagens enviadas no POST

            # Caminho do arquivo HTML da notícia com base no slug fornecido
            arquivo_html = os.path.join(settings.BASE_DIR, f'trendfeeds/templates/html/noticias/{slug}.html')

            # Verifica se o arquivo HTML existe, se não, retorna erro
            if not os.path.exists(arquivo_html):
                return JsonResponse({'success': False, 'error': 'Arquivo HTML não encontrado.'})

            # Abre e lê o conteúdo do arquivo HTML
            with open(arquivo_html, 'r', encoding='utf-8') as arquivo:
                conteudo_arquivo = arquivo.read()

            # Atualiza o título da notícia no conteúdo do arquivo HTML
            if titulo:
                conteudo_arquivo = re.sub(
                    r'{% block second_title %}.*?{% endblock second_title %}',
                    f'{{% block second_title %}}{titulo}{{% endblock second_title %}}',
                    conteudo_arquivo,
                    flags=re.DOTALL
                )

            # Define o diretório de imagens da notícia
            pasta_imagens = os.path.join(settings.MEDIA_ROOT, "noticias")
            os.makedirs(pasta_imagens, exist_ok=True)  # Garante que a pasta existe

            # Obtém a lista de arquivos existentes com o mesmo slug para gerar nomes únicos para as imagens
            arquivos_existentes = [f for f in os.listdir(pasta_imagens) if f.startswith(slug)]
            indice_atual = len(arquivos_existentes)  # Conta o número de imagens existentes com o mesmo slug

            # Substitui os placeholders de imagens no conteúdo da notícia
            for imagem_id, imagem_file in imagens_alteradas.items():
                # Cria um nome único para a imagem baseada no índice atual
                nome_imagem = f"{slug}_{indice_atual}.jpg"
                caminho_imagem = os.path.join(pasta_imagens, nome_imagem)

                # Salva a imagem no diretório correto
                with open(caminho_imagem, 'wb') as destino:
                    for chunk in imagem_file.chunks():
                        destino.write(chunk)

                # Incrementa o índice para a próxima imagem
                indice_atual += 1

                # Substitui o placeholder da imagem pelo HTML da imagem com o caminho correto
                conteudo = conteudo.replace(
                    f'<imagem_id:{imagem_id}>',
                    f'<div class="div-imagem"><img class="noticia-imagem" src="{settings.MEDIA_URL}noticias/{nome_imagem}" alt="Imagem"></div>'
                )

            # Atualiza o conteúdo principal da notícia no arquivo HTML
            conteudo_arquivo = re.sub(
                r'{% block main_content %}.*?{% endblock main_content %}',
                f'{{% block main_content %}}{conteudo}{{% endblock main_content %}}',
                conteudo_arquivo,
                flags=re.DOTALL
            )

            # Salva o arquivo HTML atualizado
            with open(arquivo_html, 'w', encoding='utf-8') as arquivo:
                arquivo.write(conteudo_arquivo)

            # Retorna resposta JSON indicando sucesso
            return JsonResponse({'success': True, 'message': 'Notícia atualizada com sucesso!'})

        except Exception as e:
            # Caso ocorra algum erro, retorna uma resposta JSON com o erro
            return JsonResponse({'success': False, 'error': f'Erro ao salvar: {e}'})

    # Retorna erro se o método da requisição não for POST
    return JsonResponse({'success': False, 'error': 'Método inválido.'})










''' Função para criar novas notícias. '''
def criar_noticia(request):
    if request.method == 'POST':
        form = NoticiasForm(request.POST, request.FILES)
        if form.is_valid():
            # Salva a notícia no banco de dados
            noticia = form.save(commit=False)  # Não salva ainda no banco

            descricao_completa = noticia.descricao  # Armazena o texto completo
            noticia.descricao = descricao_completa[:93]  # Limita a descrição para o banco
            noticia.save()  # Salva a notícia com a descrição truncada

            # Salva as categorias selecionadas no formulário
            form.save_m2m()  # Salva as relações Many-to-Many, como categorias

            # Diretório de destino das imagens
            diretorio_imagens = os.path.join(settings.MEDIA_ROOT, 'noticias')
            os.makedirs(diretorio_imagens, exist_ok=True)

            try:
                # Obtém a imagem enviada
                imagem = request.FILES.get('imagens')  # Supondo que o campo no formulário seja 'imagens'

                if imagem:
                    # Define o caminho e nome do arquivo para salvar a imagem localmente
                    nome_arquivo_imagem = os.path.join(diretorio_imagens, f"n_{noticia.id}_0.jpg")

                    # Salva a imagem no diretório de destino
                    with open(nome_arquivo_imagem, 'wb') as file:
                        for chunk in imagem.chunks():
                            file.write(chunk)

                    print(f"✅ Imagem salva como {nome_arquivo_imagem}")
            except Exception as e:
                print(f"Erro ao salvar a imagem: {e}")

            # Busca a categoria relacionada à notícia
            categoria_relacionada = CategoriaNoticias.objects.filter(noticia=noticia).first()
            nome_categoria = categoria_relacionada.categoria.nome_categoria if categoria_relacionada else "Sem Categoria"

            # Diretório onde o HTML será salvo
            templates_dir = os.path.join(settings.BASE_DIR, 'trendfeeds/templates/html/noticias')
            os.makedirs(templates_dir, exist_ok=True)

            # Nome do arquivo HTML baseado no slug
            html_file_name = f'{noticia.slug}.html'
            html_file_path = os.path.join(templates_dir, html_file_name)

            # Processa a descrição para transformar quebras de linha em parágrafos
            descricao_formatada = ''.join(f"<p class='noticia-conteudo'>{linha}</p>" for linha in descricao_completa.split('\n') if linha.strip())

            # Adiciona a imagem ao conteúdo
            imagem_html = (
                f"<div class='div-imagem'><img class='noticia-imagem' src='{settings.MEDIA_URL}noticias/{f'n_{noticia.id}_0.jpg'}' alt='Imagem'></div>"
                if imagem else ""
            )

            # Conteúdo do arquivo HTML
            html_content = f"""
            {{% extends "html/modelo.html" %}}
            {{% load static %}}

            {{% block title %}}{nome_categoria}{{% endblock title %}}
            {{% block main_title %}}{nome_categoria}{{% endblock main_title %}}
            {{% block second_title %}}{noticia.titulo}{{% endblock second_title %}}
            {{% block main_content %}}
            {descricao_formatada}
            {imagem_html}
            {{% endblock main_content %}}
            """

            # Salva o conteúdo no arquivo HTML
            with open(html_file_path, 'w', encoding='utf-8') as html_file:
                html_file.write(html_content)

            # Sucesso
            messages.success(request, f'Notícia \"{noticia.titulo}\" criada com sucesso! Página gerada em {html_file_path}.')
        else:
            messages.error(request, 'Erro ao criar a notícia. Verifique os dados.')
    else:
        form = NoticiasForm()

    return render(request, 'html/criar_noticia.html', {'form': form})
    




''' Função para deletar comentários dentro da notícia, precisando estar logado. '''
@login_required
def deletar_comentario(request, comentario_id):
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para deletar comentários.")
        return redirect('detalhes_noticia', slug=request.POST.get('slug'))  # Redireciona de volta à página

    comentario = get_object_or_404(Comentario, id=comentario_id)
    slug = comentario.noticia.slug  # Obtém o slug da notícia associada ao comentário
    comentario.delete()
    messages.success(request, "Comentário deletado com sucesso.")
    return redirect('detalhes_noticia', slug=slug)  # Redireciona para os detalhes da notícia





''' Função para deletar notícias, precisando estar logado. '''
@login_required
def deletar_noticia(request, noticia_id):
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para deletar notícias.")
        return redirect('pagina_noticias_funcionarios')  # Redireciona de volta à página

    # Busca a notícia ou retorna 404 se não existir
    noticia = get_object_or_404(Noticias, id=noticia_id)
   
  

    # Caminho do template HTML baseado no slug da notícia
    nome_arquivo_html = os.path.join(settings.BASE_DIR, 'trendfeeds', 'templates', 'html', 'noticias', f"{noticia.slug}.html")

    
    try:
        # Remove o arquivo HTML se existir
        if os.path.exists(nome_arquivo_html):
            os.remove(nome_arquivo_html)
            messages.success(request, f"Arquivo {noticia.slug}.html deletado com sucesso.")
        else:
            messages.warning(request, f"O arquivo {noticia.slug}.html não foi encontrado.")
    except Exception as e:
        messages.error(request, f"Erro ao deletar o arquivo HTML: {e}")



    # Excluir imagens associadas à notícia
    pasta_imagens = os.path.join(settings.BASE_DIR, 'trendfeeds', 'media', 'noticias')
    prefixo_imagem = f"n_{noticia_id}_"



    # Itera sobre os arquivos na pasta de imagens
    for nome_arquivo in os.listdir(pasta_imagens):
        if nome_arquivo.startswith(prefixo_imagem):
            caminho_arquivo = os.path.join(pasta_imagens, nome_arquivo)
            os.remove(caminho_arquivo)
            print(f"✅ Imagem {caminho_arquivo} excluída com sucesso.")


<<<<<<< HEAD
=======

    pasta_imagens_thumbs = os.path.join(settings.BASE_DIR, 'trendfeeds', 'media', 'thumbs')
    prefixo_imagem_thumb = f"thumb_n_{noticia_id}_"


      # Itera sobre os arquivos na pasta de imagens
    for nome_arquivo in os.listdir(pasta_imagens_thumbs):
        if nome_arquivo.startswith(prefixo_imagem_thumb):
            caminho_arquivo = os.path.join(pasta_imagens_thumbs, nome_arquivo)
            os.remove(caminho_arquivo)
            print(f"✅ Imagem {caminho_arquivo} excluída com sucesso.")

>>>>>>> 14d5c0173c95180a533e27988c634c59b03f33e1
 
    # Deleta a notícia (as relações na tabela intermediária CategoriaNoticias serão deletadas automaticamente se configuradas corretamente)
    noticia.delete()

    # Mensagem de sucesso para deletar a notícia
    messages.success(request, "Notícia deletada com sucesso.")
    return redirect('pagina_noticias_funcionarios')






