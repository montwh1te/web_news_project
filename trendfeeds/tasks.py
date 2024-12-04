''' **BIBLIOTECAS PADRÃO**  '''
# Para manipular e interagir com o sistema de arquivos.
import os 

# Para trabalhar com expressões regulares.
import re  

# Para pausar a execução do programa.
import time  

# Para normalizar strings, removendo acentos e caracteres especiais.
import unicodedata  

# Para manipulação e redimensionamento de imagens.
from PIL import Image  




''' **BIBLIOTECAS DE TERCEIROS**  '''
# Importa a biblioteca `requests`, que é usada para fazer requisições HTTP em Python.
import requests  

# Importa o `webdriver` do Selenium, usado para controlar o navegador de forma automatizada.
from selenium import webdriver  

# Importa a classe `Service` do Selenium para configurar o caminho do driver do Chrome.
from selenium.webdriver.chrome.service import Service  

# Importa a classe `By`, usada para localizar elementos na página por diferentes métodos (por exemplo, ID, CLASS_NAME).
from selenium.webdriver.common.by import By  

# Importa `WebDriverWait` do Selenium para criar esperas explícitas, ou seja, aguardar a condição de um elemento ser atendida.
from selenium.webdriver.support.ui import WebDriverWait  

# Importa `expected_conditions` do Selenium, que fornece condições como visibilidade de elementos, necessárias para as esperas.
from selenium.webdriver.support import expected_conditions as EC  

# Importa `BeautifulSoup` da biblioteca `bs4` para analisar e extrair dados de documentos HTML.
from bs4 import BeautifulSoup  

# Importa `Fore`, `Style` e `init` da biblioteca `colorama` para adicionar cores e estilo ao texto exibido no terminal.
from colorama import Fore, Style, init  

# Importa a exceção `TimeoutException` do Selenium, que é levantada quando o tempo de espera de uma ação expira.
from selenium.common.exceptions import TimeoutException




''' **IMPORTAÇÕES DO DJANGO**  '''
# Importa o módulo `django` para configurar o ambiente Django, útil quando o ambiente não está rodando via servidor padrão.
import django  

# Importa o objeto `settings` do Django, permitindo acessar as configurações do projeto, como `MEDIA_URL`, onde ficam os arquivos estáticos e de mídia.
from django.conf import settings  

# Importa a função `mark_safe` da biblioteca `django.utils.safestring`, que é usada para marcar strings como seguras, permitindo que elas sejam renderizadas como HTML em templates.
from django.utils.safestring import mark_safe  

# Importa o módulo `timezone` do Django, utilizado para manipular datas e fusos horários no framework.
from django.utils import timezone  





''' **IMPORTAÇÕES DE MÓDULOS INTERNOS**  '''
# Importa os modelos `Noticias`, `Categoria` e `CategoriaNoticias` do aplicativo `trendfeeds`, usados para manipular dados no banco de dados.
from trendfeeds.models import Noticias, Categoria, CategoriaNoticias  




''' **CONFIGURAÇÃO DO AMBIENTE DJANGO E INICIALIZAÇÃO DO SELENIUM**  '''
# Define a variável de ambiente `DJANGO_SETTINGS_MODULE` para informar ao Django qual arquivo de configurações usar.
# 'web_news.settings' configura o Django para que ele utilize as configurações especificadas no arquivo 'web_news.settings'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_news.settings')

# Inicializa o Django, fazendo com que todas as funcionalidades e configurações do Django fiquem disponíveis para o script atual.
django.setup()

# Inicializa o `colorama`, configurando o terminal para resetar as cores automaticamente após cada linha de código.
init(autoreset=True)

# Define o driver do Selenium como `None`, indicando que ele ainda não foi inicializado e será configurado posteriormente.
driver = None




def coletar_noticias():

    ''' **SEÇÃO PARA AS CONFIGURAÇÕES INICIAS DA CAPTURA DE NOTÍCIAS ** '''

    # Cria uma instância de `Service` para controlar o navegador Chrome com o Selenium.
    # O parâmetro em branco indicaria que o caminho do driver do Chrome precisa ser fornecido.
    service = Service('')

    # Configura as opções do navegador Chrome, como permitir a execução em segundo plano ou desabilitar notificações.
    options = webdriver.ChromeOptions()

    # Inicializa o driver do Chrome com as opções e o serviço especificados, permitindo que o Selenium controle o navegador.
    driver = webdriver.Chrome(service=service, options=options)

    # Define a URL do site principal de notícias, que será acessada para coletar informações.
    url_principal = 'https://ge.globo.com/'

    # Inicializa um conjunto para armazenar as URLs de notícias já processadas, evitando que a mesma notícia seja coletada mais de uma vez.
    processed_urls = set()

    # Define a posição inicial de rolagem da página como 0, e prepara o incremento da rolagem em 550 pixels.
    # Isso permite simular a rolagem da página para carregar mais conteúdo.
    current_scroll_position = 0

    # Define o valor de incremento da rolagem, ou seja, quantos pixels o navegador vai rolar a cada etapa.
    scroll_increment = 550

    # Inicializa o contador para rastrear o número de notícias coletadas e garantir que o processo está avançando conforme esperado.
    contador = 0




    ''' **SEÇÃO QUE INICIA A ENTRADA NO SITE, PARA A CAPTURA OU NÃO DA NOTÍCIA** '''

    try:
        # Acessa a URL principal com o Selenium.
        driver.get(url_principal)

        # Inicia um loop para coletar notícias. A iteração será feita 30 vezes.
        for i in range(30):

            # Marca a criação de notícia como 'não', para registrar se uma notícia foi processada com sucesso.
            criado = 'nao'

            # Pausa de 2 segundos para garantir que a página carregue antes de interagir.
            time.sleep(2)

            # Atualiza a posição de rolagem da página e rola a janela para carregar mais conteúdo.
            current_scroll_position += scroll_increment
            driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")

            # Aguarda mais 2 segundos após a rolagem.
            time.sleep(2)

            # Aguarda até que os elementos de notícias estejam visíveis na página.
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'feed-post-body'))
            )

            # Encontra todos os elementos que contêm o conteúdo das notícias.
            noticias = driver.find_elements(By.CLASS_NAME, 'feed-post-body')


            try:

                # Seleciona a notícia atual para processamento.
                noticia = noticias[i]
            except IndexError:

                # Exibe mensagem de erro caso o índice esteja fora do alcance.
                print(Fore.RED + f"⚠️ Erro: Índice {i} fora do alcance para a lista de notícias. Total disponível: {len(noticias)}")
                continue




            ''' **SEÇÃO PARA VERIFICAR SE HAVERÁ OU NÃO A CAPTURA DA NOTÍCIA** '''

            try:

                # Verifica se a notícia é marcada como "Tempo Real" e ignora se for o caso.
                tempo_real = noticia.find_element(By.CLASS_NAME, 'bstn-aovivo-label')

                print(Fore.YELLOW + f"⏩ Notícia {i+1} marcada como Tempo Real, pulando... ", '\n')
                continue
            except:
                pass

            try:
                # Captura o link e o título da notícia.
                link_noticia = noticia.find_element(By.CLASS_NAME, 'feed-post-link').get_attribute('href')
                titulo_noticia = noticia.find_element(By.CSS_SELECTOR, 'a.feed-post-link p').text.strip()
            except:

                # Exibe mensagem de erro ao capturar o link ou título da notícia.
                print(Fore.RED + f"❌ Erro ao capturar link ou título da notícia {i+1}, pulando...")
                continue

            # Ignora links que contenham "/video", "/jogo", "/playlist" e URLs já processadas.
            if any(substring in link_noticia for substring in ["/video", "/jogo", "/playlist"]) or link_noticia in processed_urls:
                print(Fore.CYAN + f"⏩ Notícia {i+1} contém um link que será ignorado.", '\n')
                continue

            # Adiciona o link ao conjunto de URLs processadas.
            processed_urls.add(link_noticia)

            # Exibe o título e link da notícia capturada no console.
            print(Fore.GREEN+ "✅ " + Style.RESET_ALL + f"Notícia{i+1}: " + Fore.GREEN + f" {titulo_noticia}")
            print(Fore.BLUE + "🔗 " + Style.RESET_ALL + "Link: " + Fore.BLUE + f"{link_noticia}\n")

            # Acessa a URL da notícia para capturar o conteúdo completo.
            driver.get(link_noticia)

            try:
                # Aguarda até que o elemento de classificação esteja visível na página, indicando que é uma página de classificação.
                de_a_nota = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'voce-da-nota__container'))
                )

                print(Fore.RED + f"❌ Erro na notícia {i+1}, é uma classificação...")
                continue  
            except TimeoutException:
                # Se o elemento não for encontrado, o código continuará normalmente.
                pass  

            try:

                # Aguarda até que o título da notícia esteja visível.
                title_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'content-head__title'))
                )

                # Captura o título da notícia exibido na página.
                title_text = title_element.text
            except:

                # Exibe mensagem de erro ao capturar o título da notícia e retorna à página principal.
                print(Fore.RED + f"❌ Erro ao capturar o título da notícia {i+1}, retornando para a página principal...")

                driver.get(url_principal)
                time.sleep(2)
                continue

            try:

                # Aguarda até que o conteúdo principal da notícia esteja visível.
                content_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'mc-body'))
                )

                # Captura o conteúdo principal da notícia.
                content_text = content_element.text

                # Lista de classes de elementos a serem removidos do conteúdo.
                classes_para_remover = [
                    'content-unordered-list', 
                    'content-publication-data__from', 
                    'next-article__wrapper-header-title',
                    'js-next-article-desktop-link', 
                    'glbComentarios-initCommentButton', 
                    'shadow-video-flow-video-infocategory',
                    'visually-hidden', 
                    'content-votetitle', 
                    'content-vote__row', 
                    'shadow-video-flow-video-info__title',
                    'ellipsis-overflowing-child', 
                    'shadow-video-flow-video-infoissued', 
                    'entitieslist-itemLink',
                    'content-publication-data__updated'
                    'show-multicontent-playlist__label'
                ]

                # Remove o texto de elementos indesejados do conteúdo.
                for class_name in classes_para_remover:
                    try:
                        elemento_para_remover = content_element.find_element(By.CLASS_NAME, class_name)
                        content_text = content_text.replace(elemento_para_remover.text, "")
                    except:
                        pass

                # Exibe um resumo da notícia extraído do conteúdo principal.
                preview_content = pegar_resumo(content_text)

                print(Fore.GREEN + f"📋 Preview da notícia: {preview_content}", '\n')
            except:

                # Exibe mensagem de erro ao capturar o conteúdo da notícia e retorna à página principal.
                print(Fore.RED + f"❌ Erro ao capturar o conteúdo da notícia {i+1}, retornando para a página principal...")

                driver.get(url_principal)
                time.sleep(2)
                continue




            ''' **SEÇÃO PARA FORMATAÇÃO DO TÍTULO DA NOTÍCIA** '''

            # Normaliza o título para remover acentuação e caracteres especiais.
            titulo_normalizado = unicodedata.normalize('NFD', title_text)

            # Remove acentos do título.
            titulo_sem_acento = ''.join([c for c in titulo_normalizado if unicodedata.category(c) != 'Mn'])

            # Remove pontuação do título.
            titulo_sem_pontuacao = re.sub(r'[{}%@#$%^&*()!<>:"/\\|+_=,.?;^~`-]', '', titulo_sem_acento)

            # Formata o título para uso como identificador, substituindo espaços por underline.
            titulo_formatado_semespaco = re.sub(r'[\\/*?:"<>|]', "", titulo_sem_pontuacao).replace(" ", "_")

            # Substitui caracteres específicos para manter compatibilidade com sistemas de arquivos.
            titulo_formatado_semespaco = titulo_formatado_semespaco.replace("º", "o")
            titulo_formatado_semespaco = titulo_formatado_semespaco.replace("ª", "a")

            # Trunca o título para 200 caracteres em minúsculas.
            titulo_truncado = titulo_formatado_semespaco[:200].lower()




            ''' **SEÇÃO PARA MANIPULAÇÃO DE ARQUIVOS DE IMAGENS**  '''

            # Diretório absoluto para salvar as imagens da notícia.
            diretorio_imagens = settings.MEDIA_ROOT

            # Cria o diretório de imagens se ele ainda não existir.
            os.makedirs(diretorio_imagens, exist_ok=True)

            # Formata o título da notícia para uso futuro.
            titulo_formatado = re.sub(r'[\\/*?:"<>|]', "", title_text)

        


            times = { 
                     
            # Times Série A 
            "atletico_mg": ["atleticomg", "galo"], "athletico_pr": ["atleticopr", "athletico", "furacao"], "bahia": ["bahia", "esquadrao", "esquadrao de aco"], "botafogo": ["botafogo", "fogao"], "bragantino": ["bragantino", "red bull bragantino", "massa bruta"], "corinthians": ["corinthians", "timao"], "cruzeiro": ["cruzeiro", "raposa"], "cuiaba": ["cuiaba", "dourado"], "flamengo": ["flamengo", "fla", "urubu"], "fluminense": ["fluminense", "flu", "tricolor das laranjeiras"], "fortaleza": ["fortaleza", "leao do pici"], "gremio": ["gremio", "tricolor gaucho", "imortal"], "internacional": ["inter", "colorado"], "palmeiras": ["palmeiras", "verdao"], "sao_paulo": ["sao paulo", "spfc", "tricolor paulista"], "vasco": ["vasco", "vascao", "gigante da colina"], "juventude": ["juventude", "juve"], "criciuma": ["criciuma", "tigre"], "vitoria": ["vitoria", "leao da barra"], "atletico_go": ["atleticogo", "dragao"], 
            
            # Seleção Brasileira 
            "selecao": ["selecao", "selecao brasileira", "canario", "canarinho"], 
            
            # Times Série B
            "ceara": ["ceara", "vozao"], "crb": ["crb"], "amazonas": ["amazonas", "onca pintada"], "operario_pr": ["operariopr", "operario", "fantasma"], "brusque": ["brusque", "maior do vale", "bruscao", "marreco"], "paysandu": ["paysandu", "papao"], "chapecoense": ["chapecoense", "chape"], "ituano": ["ituano", "galo de itu"], "mirassol": ["mirassol", "leao"], "novorizontino": ["novorizontino", "tigre do vale"], "ponte_preta": ["ponte preta", "macaca"], "sport": ["sport", "leao da ilha"], "vila_nova": ["vila nova", "tigre"], "avai": ["avai", "leao da ilha"], "botafogo_sp": ["botafogosp", "pantera"], "guarani": ["guarani", "bugre"], "goias": ["goias", "esmeraldino"], "santos": ["santos", "peixe"], "coritiba": ["coritiba", "coxa"], "america_mg": ["americamg", "coelho"], 
            }




            ''' **SEÇÃO DE CRIAÇÃO E ATUALIZAÇÃO DA NOTÍCIA NO BANCO DE DADOS** '''

            try:            

                 #pega a data atual para salvar no banco
                data_publicacao = timezone.now()

                #o autor permanece desconhecido caso nao seja encontrado na noticia
                autor_text = "Desconhecido"

                try:
                    autor_element = driver.find_element(By.CLASS_NAME, 'content-author__name')
                    autor_text = autor_element.text
                except:
                    pass

                # Cria ou atualiza a notícia e salva no banco de dados
                noticia_modelo, created = Noticias.objects.update_or_create(
                    titulo=titulo_truncado,
                    defaults={
                        'data_publicacao': data_publicacao,
                        'descricao': preview_content,
                        'autor': autor_text,
                        'link': link_noticia
                    }
                )
                print(Fore.GREEN + f"Notícia '{titulo_truncado}' {'criada' if created else 'atualizada'} no banco de dados com sucesso.")


                # Procura por categorias na lista de times com base no título da notícia
                categorias_encontradas = []

                #o time_id permanece none se ele nao conseguir associar
                time_id = None

                # Quebra o título em palavras para preservar a ordem
                palavras_titulo = titulo_sem_pontuacao.lower().split()




                ''' **SEÇÃO DE VERIFICAÇÃO DA CATEGORIA DA NOTÍCIA** '''

                # Itera sobre as palavras do título, priorizando a ordem natural do texto
                for palavra in palavras_titulo:
                    for clube, dados in times.items():

                        # Verifica se a palavra é um apelido do time
                        if palavra in dados[:-1]:  

                            # Se nenhuma categoria foi registrada
                            if not categorias_encontradas:  
                                categorias_encontradas.append(clube)

                                # Atribui o ID do time correspondente
                                time_id = dados[-1]

                                # Para de buscar após encontrar o primeiro time
                                break  

                    # Se já encontrou uma categoria, para de iterar
                    if categorias_encontradas:  
                        break
                print(Fore.BLUE + f"🔍 Categoria escolhida: {categorias_encontradas[0] if categorias_encontradas else 'Nenhuma'}", '\n')


                # Verifica se nenhuma categoria foi encontrada no título da notícia.
                if len(categorias_encontradas) == 0:  

                    # Exibe uma mensagem de aviso no console informando que nenhuma categoria foi associada.
                    print(Fore.YELLOW + "⚠️ Não foi possível relacionar nenhuma categoria!", '\n') 

                    # Busca ou cria uma categoria padrão chamada 'outros' no banco de dados.
                    categoria, _ = Categoria.objects.get_or_create(nome_categoria='outros')  

                    # Cria uma associação entre a notícia e a categoria 'outros'.
                    CategoriaNoticias.objects.get_or_create(noticia=noticia_modelo, categoria=categoria)  

                # Se ao menos uma categoria foi encontrada:
                else:  

                    # Verifica novamente se há categorias encontradas (redundante neste caso, mas usado por segurança).
                    if categorias_encontradas:  
                        
                        # Itera sobre todas as categorias encontradas no título da notícia.
                        for nome_categoria in categorias_encontradas:  
                            
                            # Busca ou cria cada categoria encontrada no banco de dados.
                            categoria, _ = Categoria.objects.get_or_create(nome_categoria=nome_categoria)  

                            # Associa a notícia à categoria encontrada.
                            CategoriaNoticias.objects.get_or_create(noticia=noticia_modelo, categoria=categoria)  

                    print(Fore.GREEN + f"Notícia '{titulo_truncado}' associada com a categoria '{categoria.nome_categoria}'.", '\n')  

            # Exibe uma mensagem no console informando que a notícia foi associada com sucesso a uma ou mais categorias.
            except Exception as e:
                print(Fore.YELLOW + "⚠️ Não foi possível relacionar nenhuma categoria!", '\n')
                



            # Obtenha o ID gerado
            novo_id_noticia = noticia_modelo.id  
               



            ''' **SEÇÃO PARA PEGAR AS IMAGENS DA NOTÍCIA** '''

            try:

                # Localiza todos os elementos de imagem na página com o seletor CSS "amp-img".
                imagens_elementos = WebDriverWait(driver, 60).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "amp-img")))
                
                # Inicializa uma lista vazia para armazenar os URLs das imagens.
                imagem_urls = []

                # Itera sobre cada elemento de imagem encontrado, com um índice `j` para diferenciar as imagens.
                for j, imagem_elemento in enumerate(imagens_elementos):
                    try:
                        # Aguarda o carregamento do atributo `src`.
                        WebDriverWait(driver, 10).until(
                            lambda d: imagem_elemento.get_attribute("src") is not None)

                        # Obtém o atributo `src` de cada elemento de imagem, que contém o URL da imagem.
                        url_imagem = imagem_elemento.get_attribute("src")

                        # Valida o URL da imagem (opcionalmente, pode filtrar URLs inválidos).
                        if not url_imagem or not url_imagem.startswith("http"):
                            print(Fore.RED + f"⚠️ URL inválido encontrado: {url_imagem}")
                            continue

                        # Define o caminho e nome do arquivo para salvar a imagem localmente, com base no ID da notícia e no índice.
                        nome_arquivo_imagem = os.path.join(f'{diretorio_imagens}/noticias', f"n_{novo_id_noticia}_{j}.jpg")

                        # Verifica se o arquivo já existe.
                        if os.path.exists(nome_arquivo_imagem):
                            print(Fore.YELLOW + f"🔄 Arquivo {nome_arquivo_imagem} já existe. Será sobrescrito.")
                                
                        # Faz uma requisição HTTP para o URL da imagem e ativa o modo "stream" para download por partes.
                        resposta_imagem = requests.get(url_imagem, stream=True)

                        # Verifica se a requisição foi bem-sucedida. Lança uma exceção caso haja algum erro (e.g., 404 ou 500).
                        resposta_imagem.raise_for_status()

                        # Abre um arquivo no modo "write binary" para salvar os dados da imagem.
                        with open(nome_arquivo_imagem, 'wb') as file:

                            # Faz o download da imagem em blocos de 1024 bytes para economizar memória.
                            for chunk in resposta_imagem.iter_content(1024):

                                # Escreve cada bloco baixado no arquivo.
                                file.write(chunk)

                        # Adiciona o caminho da imagem salva à lista `imagem_urls`.
                        imagem_urls.append(nome_arquivo_imagem)

                        # Exibe uma mensagem indicando que a imagem foi salva com sucesso.
                        print(Fore.GREEN + f"✅ Imagem {j} salva como {nome_arquivo_imagem}")

                        # Redimensiona a imagem e salva no diretório de miniaturas (thumbs)
                        # Define o caminho e nome do arquivo para salvar a miniatura da imagem.
                        nome_arquivo_thumb = os.path.join(f'{diretorio_imagens}/thumbs', f"thumb_n_{novo_id_noticia}.jpg")
                        
                        # Abre a imagem salva usando a biblioteca Pillow.
                        with Image.open(nome_arquivo_imagem) as img:

                            # Redimensiona a imagem para um tamanho máximo de 380x215 pixels, mantendo a proporção.
                            img.thumbnail((380, 215))

                            # Salva a miniatura no formato JPEG no diretório definido.
                            img.save(nome_arquivo_thumb, "JPEG")
                        # Exibe uma mensagem indicando que a miniatura foi salva com sucesso.

                        print(Fore.GREEN + f"✅ Miniatura da imagem {j} salva como {nome_arquivo_thumb}")

                    except Exception as e:

                        # Exibe uma mensagem de erro caso qualquer exceção seja levantada durante o processo.
                        print(Fore.RED + f"Erro ao baixar as imagens: {e}")

            except Exception as e:

                # Exibe uma mensagem de erro geral caso qualquer exceção seja levantada.
                print(Fore.RED + f"Erro ao baixar as imagens: {e}")
                                



            ''' **SEÇÃO QUE CRIA A PRIMEIRA BASE HTML DA NOTÍCIA** '''

            nome_arquivo = f"{titulo_truncado}.html"

            # Define o nome do arquivo e o caminho para salvar o HTML da notícia.
            caminho_arquivo = os.path.join('trendfeeds/templates/html/noticias', nome_arquivo)

            # Cria o conteúdo HTML para a notícia.
            html_content = f"""
            <html>
                <article class="noticia-detalhada">
                    <h1 class="noticia-titulo mt-4">{title_text}</h1>
                    <p class="noticia-conteudo">{content_text}</p>
                </article>
            </html>
            """
            
            # Salva o HTML da notícia no diretório especificado.
            with open(caminho_arquivo, 'w', encoding='utf-8') as file:
                file.write(html_content)

            # Marca a notícia como criada.
            print(Fore.GREEN + f"✅Arquivo HTML criado com sucesso: {caminho_arquivo}", '\n')
            criado = 'sim'

            second_title_formatado = re.sub(r'[\\/*?:"<>|]', "", title_text)
            main_content_formatado = formatar_texto(titulo_formatado_semespaco, imagens_elementos, novo_id_noticia)

            # Atualiza o caminho do arquivo HTML da notícia.
            caminho_arquivo = os.path.join('trendfeeds/templates/html/noticias', nome_arquivo)
            categoria_nome = categorias_encontradas[0] if categorias_encontradas else "Outros"

            # Local para salvar as páginas de categoria
            categoria_template_dir = 'trendfeeds/templates/html/categorias'

            # Cria o diretório de categorias se ele ainda não existir
            os.makedirs(categoria_template_dir, exist_ok=True)
            




            ''' **SEÇÃO QUE CRIA A PÁGINA INDEX DE CADA CATEGORIA** '''

            if categorias_encontradas:
                for nome_categoria in categorias_encontradas:
                    try:
                        # Cria ou obtém a categoria no banco de dados.
                        categoria, _ = Categoria.objects.get_or_create(nome_categoria=nome_categoria)

                        nome_amigavel = categoria.nome

                        # Associa a notícia à categoria.
                        CategoriaNoticias.objects.get_or_create(noticia=noticia_modelo, categoria=categoria)

                        # Define o nome do arquivo HTML para a página da categoria.
                        nome_arquivo_categoria = os.path.join(categoria_template_dir, f'index_{nome_categoria}.html')

                        categorias_encontradas = []
                        time_id = None

                        # Verifica se o arquivo existe; caso contrário, cria a página
                        if not os.path.exists(nome_arquivo_categoria):
                            html_categoria_content = f"""
{{% extends "html/modelo_categoria.html" %}}
{{% load static %}}

{{% block title %}}{categoria.nome_categoria}{{% endblock title %}}
{{% block main_title %}}{categoria.nome_categoria}{{% endblock main_title %}}
{{% block id_time %}}{time_id}{{% endblock id_time %}}

<div class="categoria-listagem">
    <h2>Últimas notícias sobre {categoria.nome_categoria}</h2>
    <p>Aqui você encontrará todas as notícias sobre {categoria.nome_categoria}.</p>
</div>
                            """
                        
                            # Salva o conteúdo da página de categoria no arquivo.
                            with open(nome_arquivo_categoria, "w", encoding="utf-8") as file:
                                file.write(html_categoria_content)
                                
                            # Exibe mensagem de sucesso para criação da página de categoria.
                            print(Fore.GREEN + f"📂 Página da categoria '{categoria.nome_categoria}' criada com sucesso em: {nome_arquivo_categoria}")
                        else:

                            # Notifica que a página já existe e não será recriada.
                            print(Fore.YELLOW + f"⚠️ A página da categoria '{categoria.nome_categoria}' já existe. Não será criada novamente.")

                    except Exception as e:

                        # Exibe mensagem de erro ao criar a página da categoria.
                        print(Fore.RED + f"❌ Erro ao criar a página da categoria '{categoria.nome_categoria}': {e}")
            else:

                # Exibe mensagem ao não encontrar categorias para a notícia.
                print(Fore.RED + "⚠️ Nenhuma categoria encontrada! Atribuindo à categoria 'Outros'.", '\n', '\n')





            ''' **SEÇÃO QUE CRIA A SEGUNDA BASE HTML DA NOTÍCIA** '''

            # Cria o conteúdo HTML para a notícia, referenciando o template principal.
            html_content = f"""
            
{{% extends "html/modelo.html" %}}
{{% load static %}}

{{% block title %}}{categoria.nome_categoria}{{% endblock title %}}
{{% block main_title %}}{categoria.nome_categoria}{{% endblock main_title %}}
{{% block second_title %}}{second_title_formatado}{{% endblock second_title %}}
{{% block main_content %}}{main_content_formatado}{{% endblock main_content %}}

"""

            # Incrementa o contador se o arquivo foi criado.
            if criado == 'sim':
                contador += 1

            # Encerra o loop após processar X notícias.
            if contador == 99:
                break
                                
             # Salva o conteúdo renderizado no HTML.
            with open(caminho_arquivo, "w", encoding="utf-8") as file:
                file.write(html_content)

            # Retorna à página principal e aguarda o carregamento.
            driver.get(url_principal)
            time.sleep(2)
    finally:

        # Encerra o navegador, independentemente de o resultado do processamento.
        driver.quit()

        # Exibe mensagem indicando que o navegador foi fechado.
        print(Fore.GREEN + "🛑 Navegador encerrado. Coleta finalizada.")





def pegar_resumo(texto):
    ''' 
    Função que recebe um texto e retorna o resumo, que é a primeira linha do texto.
    A primeira linha é definida como o trecho de texto antes da primeira quebra de linha.
    '''
    
    # Divide o texto na primeira ocorrência de quebra de linha e retorna a primeira parte.
    primeira_linha = texto.split('\n', 1)[0]  

    # Remove espaços em branco no início e no final da primeira linha antes de retornar.
    return primeira_linha.strip()  





def formatar_texto(arquivo_nome, imagens_elementos, novo_id_noticia):
    ''' 
    Função que recebe o nome de um arquivo, elementos de imagem e um novo ID de notícia.
    A função processa o conteúdo do arquivo, realiza a formatação do texto removendo 
    tags HTML, emojis e outras informações irrelevantes, e o converte para HTML.
    '''

    # Define o nome do arquivo e o caminho para buscá-lo.
    nome_arquivo = arquivo_nome
    file_path = os.path.join('trendfeeds', 'templates', 'html', 'noticias', f'{arquivo_nome}.html')
    
    # Verifica se o arquivo existe e captura seu conteúdo, caso contrário, inicializa com texto vazio.
    if __verificar_caminho(arquivo_nome, file_path): 
        text = __captar_tag(file_path)
    else:
        text = ""
    
    # Se o conteúdo do arquivo não estiver vazio, realiza a formatação.
    if text:
        # Remove todas as tags HTML do texto.
        text = re.sub(r'<[^>]+>', '', text)
        print("✅ Tags HTML removidas do texto!")

        # Remove frases que começam com "+" seguido por texto até o final da linha.
        text = re.sub(r'\+ [^\n]+', '', text)
        
        # Define um padrão para capturar linhas que começam e terminam com emojis.
        emoji_pattern = re.compile(
            r'^[\U0001F600-\U0001F64F].*?[\U0001F600-\U0001F64F]$'
            r'|^[\U0001F300-\U0001F5FF].*?[\U0001F300-\U0001F5FF]$'
            r'|^[\U0001F680-\U0001F6FF].*?[\U0001F680-\U0001F6FF]$'
            r'|^[\U0001F700-\U0001F77F].*?[\U0001F700-\U0001F77F]$'
            r'|^[\U0001F780-\U0001F7FF].*?[\U0001F780-\U0001F7FF]$'
            r'|^[\U0001F800-\U0001F8FF].*?[\U0001F800-\U0001F8FF]$'
            r'|^[\U0001F900-\U0001F9FF].*?[\U0001F900-\U0001F9FF]$'
            r'|^[\U0001FA00-\U0001FA6F].*?[\U0001FA00-\U0001FA6F]$'
            r'|^[\U0001FA70-\U0001FAFF].*?[\U0001FA70-\U0001FAFF]$'
            r'|^[\U00002700-\U000027BF].*?[\U00002700-\U000027BF]$'
            r'|^[\U0001F1E0-\U0001F1FF].*?[\U0001F1E0-\U0001F1FF]$'
            , flags=re.MULTILINE
        )
        
        # Substitui linhas que começam e terminam com emojis por uma string vazia.
        text = emoji_pattern.sub('', text)
        
        # Remove frases que começam com "Assista:" e terminam com ".".
        text = re.sub(r'Assista:.*?\.', '', text)
        
        # Remove frases que começam com "Veja" e terminam com "também".
        text = re.sub(r'^Veja.*também$', '', text, flags=re.MULTILINE)
        print("✅ Texto formatado com remoção de emojis, 'Assista:' e 'Veja...também'.")
    
    # Adiciona imagens ao texto formatado.
    text = __adicionar_imagens(text, imagens_elementos, novo_id_noticia)
    
    # Divide o texto em parágrafos com base nos pontos finais.
    paragrafos = __dividir_por_pontos_finais(text, 3)
    
    # Converte os parágrafos em HTML.
    text = __criar_html_com_paragrafos(paragrafos)
    print("✅ Texto processado e convertido em HTML.")
    
    return text





def __verificar_caminho(arquivo_nome, file_path):
    ''' 
    Função que verifica se um arquivo existe no caminho especificado.
    Recebe o nome do arquivo e o caminho completo, retornando True se o arquivo for encontrado 
    e uma string vazia caso contrário. Também exibe informações sobre o processo.
    '''
    
    # Exibe uma linha de separação e uma mensagem indicando que a verificação do arquivo está em andamento.
    print('-' * 10, '🔍 VERIFICANDO A EXISTÊNCIA DO ARQUIVO', '-' * 10, '\n')
    
    # Exibe o nome do arquivo que está sendo verificado.
    print(f"📄 Recebendo título: {arquivo_nome}")

    # Verifica se o arquivo existe no caminho especificado.
    if os.path.exists(file_path):

        # Se o arquivo for encontrado, exibe uma mensagem de sucesso.
        print(Fore.GREEN + f"✅ Arquivo encontrado: {file_path}\n")
        print('-' * 30)

        # Retorna True, indicando que o arquivo foi encontrado.
        return True
    else:

        # Se o arquivo não for encontrado, exibe uma mensagem de erro.
        print(Fore.RED + f"❌ Arquivo não encontrado: {file_path}\n")
        print('-' * 30)

        # Retorna uma string vazia, indicando que o arquivo não existe.
        return ""





def __captar_tag(file_path):
    ''' 
    Função que abre um arquivo HTML, lê seu conteúdo e captura o texto da primeira tag <p> encontrada.
    Retorna o texto dessa tag, ou uma mensagem caso a tag não seja encontrada.
    '''
    
    # Inicializa uma string vazia para armazenar o conteúdo da tag <p>.
    text = ""

    # Abre o arquivo HTML especificado no caminho fornecido, com a codificação UTF-8.
    with open(file_path, 'r', encoding='utf-8') as file:
        # Lê o conteúdo do arquivo.
        p_content = file.read()
        # Exibe uma mensagem indicando que o arquivo foi lido com sucesso.
        print(f"📂 Arquivo lido com sucesso: {file_path}")

    # Usa o BeautifulSoup para analisar o conteúdo HTML do arquivo.
    soup = BeautifulSoup(p_content, 'lxml')

    # Busca a primeira tag <p> no conteúdo HTML.
    p_tag = soup.find('p')

    # Verifica se a tag <p> foi encontrada no conteúdo.
    if p_tag:

        # Se a tag <p> foi encontrada, armazena o texto dentro dela.
        text = p_tag.get_text()
    else:

        # Se a tag <p> não for encontrada, exibe uma mensagem de alerta.
        print("⚠️ Nenhuma tag <p> encontrada no conteúdo.")
    
    # Retorna o texto encontrado na tag <p>, ou uma string vazia caso não tenha sido encontrada.
    return text





def __dividir_por_pontos_finais(texto, num_pontos_finais):
    ''' 
    Função que divide um texto em parágrafos, agrupando as sentenças com base no número de pontos finais especificado.
    As tags de imagem são tratadas separadamente para garantir que não sejam divididas.
    '''
    
    # Encontra todas as tags <img> no texto usando expressão regular.
    img_tags = re.findall(r'<img.*?>', texto)

    # Substitui temporariamente as tags <img> por marcadores únicos para não dividi-las.
    for i, tag in enumerate(img_tags):
        texto = texto.replace(tag, f"[[IMG_TAG_{i}]]")

    # Divide o texto em sentenças, usando o ponto final como delimitador.
    sentencas = texto.split('.')
    
    # Inicializa uma lista para armazenar os parágrafos gerados.
    paragrafos = []

    # Agrupa as sentenças em parágrafos, conforme o número de sentenças definidas pelo argumento.
    for i in range(0, len(sentencas), num_pontos_finais):

        # Junta as sentenças atuais no parágrafo e adiciona um ponto final no final do parágrafo.
        paragrafo_atual = '. '.join(sentencas[i:i + num_pontos_finais]).strip() + '.'

        # Verifica se o parágrafo não está vazio ou não contém "Foto:", antes de adicioná-lo à lista de parágrafos.
        if "Foto:" in paragrafo_atual or paragrafo_atual.strip():
            paragrafos.append(paragrafo_atual)

    # Restaura as tags <img> nos parágrafos processados.
    for i, tag in enumerate(img_tags):
        paragrafos = [paragrafo.replace(f"[[IMG_TAG_{i}]]", tag) for paragrafo in paragrafos]

    # Exibe uma mensagem indicando quantos parágrafos foram gerados.
    print(f"✅ Texto dividido em {len(paragrafos)} parágrafos.")
    
    # Retorna a lista de parágrafos gerados.
    return paragrafos





def __criar_html_com_paragrafos(paragrafos):
    ''' 
    Função que converte uma lista de parágrafos em conteúdo HTML.
    Cada parágrafo é envolvido em uma tag <p> com uma classe CSS.
    '''

    # Inicializa uma string vazia para armazenar o conteúdo HTML gerado.
    html_content = ""

    # Itera sobre cada parágrafo na lista de parágrafos fornecida.
    for paragrafo in paragrafos:
        # Para cada parágrafo, cria uma tag <p> com a classe 'noticia-conteudo' e insere o parágrafo dentro dela.
        html_content += f"<p class='noticia-conteudo'>{paragrafo}</p>\n"

    # Marca o conteúdo HTML como seguro para renderização em Django.
    # Isso evita que as tags HTML sejam convertidas em texto normal (sem renderizar o HTML).
    html_content = mark_safe(html_content)

    # Retorna o conteúdo HTML formatado, pronto para ser exibido em uma página web.
    return html_content





def __adicionar_imagens(text, image_names, noticia_id):
    ''' 
    Função que adiciona imagens ao texto, vinculando as imagens às descrições no conteúdo.
    Para cada linha que contém a palavra "Foto:", uma imagem será inserida.
    O caminho da imagem é baseado no ID da notícia e no índice da imagem.

    text: O texto original onde as imagens serão inseridas.
    image_names: Lista contendo os nomes das imagens a serem inseridas.
    noticia_id: O ID único da notícia, usado para gerar o caminho das imagens.
    '''
    
    # Divide o texto em linhas, separando-o onde há quebras de linha (\n).
    # Isso ajuda a identificar partes específicas do texto onde as imagens devem ser inseridas.
    lines = text.split('\n')

    # Inicializa uma lista vazia para armazenar o novo texto com as imagens inseridas.
    new_text = []

    # Inicializa o índice para rastrear qual imagem da lista image_names está sendo inserida.
    image_index = 0

    # Itera sobre cada linha do texto original.
    for line in lines:

        # Verifica se a linha contém a palavra "Foto:" e se ainda há imagens disponíveis para adicionar.
        if "Foto:" in line and image_index < len(image_names):

            # Cria a tag HTML para a imagem, incluindo uma classe CSS para estilização.
            # Usa o ID da notícia (noticia_id) e o índice da imagem (image_index) para gerar um caminho único.
            img_tag = f'<div class="div-imagem"><img class="noticia-imagem" src="{{% get_media_prefix %}}noticias/n_{noticia_id}_{image_index}.jpg"></div>'

            # Cria uma nova linha combinando a tag de imagem com a descrição original da linha.
            new_line = f"{img_tag}<p class='foto-descricao'>{line}</p>"

            # Adiciona a nova linha (imagem + descrição) à lista de novas linhas.
            new_text.append(new_line)

            # Incrementa o índice para passar para a próxima imagem.
            image_index += 1

        # Se a linha não contiver "Foto:" ou não houver mais imagens, adiciona a linha original ao texto final.
        else:
            new_text.append(line)

    # Combina todas as linhas modificadas (com as imagens inseridas) em uma única string.
    # As linhas são separadas por quebras de linha (\n).
    final_text = '\n'.join(new_text)

    # Exibe no console o número de imagens que foram adicionadas ao texto.
    print(f"✅ {image_index} imagens adicionadas ao texto.")

    # Retorna o texto final com as tags de imagem já inseridas.
    return final_text





def iniciar_scheduler():
    ''' 
    Função responsável por iniciar o agendador de tarefas.
    Atualmente, serve como um marcador de posição (placeholder) que pode ser expandido no futuro para incluir a lógica de agendamento real.
    '''
    
    # Exibe uma mensagem no console indicando que o agendador foi iniciado.
    print("⏰ Scheduler iniciado.")

    # A função atualmente não faz nada, mas pode ser expandida no futuro com agendamentos de tarefas.
    pass

