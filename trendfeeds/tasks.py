# BIBLIOTECAS PADRÃO**
import os  
    # Para manipular e interagir com o sistema de arquivos.
import re  
    # Para trabalhar com expressões regulares.
import time  
    # Para pausar a execução do programa.
import unicodedata  
    # Para normalizar strings, removendo acentos e caracteres especiais.
from PIL import Image  
    # Para manipulação e redimensionamento de imagens.




# **BIBLIOTECAS DE TERCEIROS**
import requests  
        # Para realizar requisições HTTP.
from selenium import webdriver  
    # Para automação de navegadores web.
from selenium.webdriver.chrome.service import Service  
    # Para definir o caminho do driver Chrome.
from selenium.webdriver.common.by import By  
    # Para localizar elementos na página com métodos como CLASS_NAME e ID.
from selenium.webdriver.support.ui import WebDriverWait  
    # Para implementar esperas explícitas no Selenium.
from selenium.webdriver.support import expected_conditions as EC  
    # Para verificar condições em elementos, como visibilidade.
from bs4 import BeautifulSoup  
    # Para fazer o parsing de HTML e extrair informações de páginas web.
from colorama import Fore, Style, init  
    # Para estilizar a saída no terminal, como colorir texto.




# **IMPORTAÇÕES DO DJANGO**
import django  
    # Para configurar o ambiente Django fora do servidor padrão.
from django.conf import settings  
    # Para acessar configurações do projeto, como MEDIA_URL.
from django.utils.safestring import mark_safe  
    # Para marcar strings como seguras, permitindo HTML no template.
from django.utils import timezone  
    # Para trabalhar com datas e fusos horários no Django.




# **IMPORTAÇÕES DE MÓDULOS INTERNOS**
from trendfeeds.models import Noticias, Categoria, CategoriaNoticias  
    # Importa os modelos usados para manipular notícias e categorias no banco de dados.




# **CONFIGURAÇÃO DO AMBIENTE DJANGO E INICIALIZAÇÃO DO SELENIUM**
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_news.settings')
    # DJANGO_SETTINGS_MODULE define o caminho para o arquivo de configurações.
    # 'web_news.settings' configura o Django para que ele use as configurações especificadas no arquivo 'web_news.settings'.
django.setup()
    # Inicializa o Django, tornando disponíveis suas funcionalidades para o script atual.
init(autoreset=True)
    # Inicializa o colorama, que permite que o terminal redefina as cores após cada linha.
driver = None
    # Define o driver do Selenium como None para poder ser inicializado mais adiante.




def coletar_noticias():
    service = Service('')
        # Cria uma instância de Service para controlar o navegador Chrome pelo Selenium.
    options = webdriver.ChromeOptions()
        # Configura opções para o navegador Chrome.
    driver = webdriver.Chrome(service=service, options=options)
        # Inicializa o driver do Chrome com as configurações especificadas.


    url_principal = 'https://ge.globo.com/'
        # Define a URL do site principal de notícias que será acessado.


    processed_urls = set()
        # Inicializa um conjunto para armazenar URLs de notícias já processadas, evitando duplicações.
    current_scroll_position = 0
    scroll_increment = 550
        # Define a posição inicial de rolagem da página e o incremento de rolagem por etapa.
    contador = 0
        # Contador para rastrear o número de notícias coletadas.


    try:
        driver.get(url_principal)
            # Acessa a URL principal com o Selenium.


        for i in range(30):
            criado = 'nao'
                # Marca a criação de notícia como 'não', para registrar se uma notícia foi processada com sucesso.

            time.sleep(2)
                # Pausa de 2 segundos para garantir que a página carregue antes de interagir.

            current_scroll_position += scroll_increment
            driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")
                # Rola a página para baixo a cada ciclo para carregar novas notícias.

            time.sleep(2)
                # Aguarda mais 2 segundos após a rolagem.

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'feed-post-body'))
            )
                # Aguarda até que os elementos de notícias estejam visíveis.

            noticias = driver.find_elements(By.CLASS_NAME, 'feed-post-body')
                # Encontra todos os elementos que contêm o conteúdo das notícias.


            try:
                noticia = noticias[i]
                    # Seleciona a notícia atual para processamento.
            except IndexError:
                print(Fore.RED + f"⚠️ Erro: Índice {i} fora do alcance para a lista de notícias. Total disponível: {len(noticias)}")
                    # Exibe mensagem de erro caso o índice esteja fora do alcance.
                continue
            try:
                tempo_real = noticia.find_element(By.CLASS_NAME, 'bstn-aovivo-label')
                print(Fore.YELLOW + f"⏩ Notícia {i+1} marcada como Tempo Real, pulando... ", '\n')
                    # Ignora notícias marcadas como "Tempo Real" e passa para a próxima.
                continue
            except:
                pass
            try:
                link_noticia = noticia.find_element(By.CLASS_NAME, 'feed-post-link').get_attribute('href')
                titulo_noticia = noticia.find_element(By.CSS_SELECTOR, 'a.feed-post-link p').text.strip()
                    # Captura o link e o título da notícia.
            except:
                print(Fore.RED + f"❌ Erro ao capturar link ou título da notícia {i+1}, pulando...")
                    # Exibe mensagem de erro ao capturar o link ou título da notícia.
                continue


            if any(substring in link_noticia for substring in ["/video", "/jogo", "/playlist"]) or link_noticia in processed_urls:
                print(Fore.CYAN + f"⏩ Notícia {i+1} contém um link que será ignorado.", '\n')
                    # Ignora links que contenham "/video", "/jogo", ou "/playlist" e URLs já processadas.
                continue
            processed_urls.add(link_noticia)
                # Adiciona o link ao conjunto de URLs processadas.


            print(Fore.GREEN+ "✅ " + Style.RESET_ALL + f"Notícia{i+1}: " + Fore.GREEN + f" {titulo_noticia}")
            print(Fore.BLUE + "🔗 " + Style.RESET_ALL + "Link: " + Fore.BLUE + f"{link_noticia}\n")
                # Exibe o título e link da notícia capturada no console.

            driver.get(link_noticia)
                # Acessa a URL da notícia para capturar o conteúdo completo.


            try:
                title_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'content-head__title'))
                )
                title_text = title_element.text
                    # Captura o título da notícia exibido na página.
            except:
                print(Fore.RED + f"❌ Erro ao capturar o título da notícia {i+1}, retornando para a página principal...")
                    # Exibe mensagem de erro ao capturar o título da notícia.
                driver.get(url_principal)
                time.sleep(2)
                continue
            try:
                content_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'mc-body'))
                )
                content_text = content_element.text
                    # Captura o conteúdo principal da notícia.
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
                ]
                    # Lista de classes de elementos a serem removidos do conteúdo.
                for class_name in classes_para_remover:
                    try:
                        elemento_para_remover = content_element.find_element(By.CLASS_NAME, class_name)
                        content_text = content_text.replace(elemento_para_remover.text, "")
                            # Remove o texto de elementos indesejados do conteúdo.
                    except:
                        pass
                preview_content = pegar_resumo(content_text)
                print(Fore.GREEN + f"📋 Preview da notícia: {preview_content}", '\n')
                    # Exibe um resumo da notícia extraído do conteúdo principal.
            except:
                print(Fore.RED + f"❌ Erro ao capturar o conteúdo da notícia {i+1}, retornando para a página principal...")
                    # Exibe mensagem de erro ao capturar o conteúdo da notícia.
                driver.get(url_principal)
                time.sleep(2)
                continue


            titulo_normalizado = unicodedata.normalize('NFD', title_text)
                # Normaliza o título para remover acentuação e caracteres especiais.

            titulo_sem_acento = ''.join([c for c in titulo_normalizado if unicodedata.category(c) != 'Mn'])
                # Remove acentos do título.

            titulo_sem_pontuacao = re.sub(r'[{}%@#$%^&*()!<>:"/\\|+_=,.?;^~`-]', '', titulo_sem_acento)
                    # Remove pontuação do título.

            titulo_formatado_semespaco = re.sub(r'[\\/*?:"<>|]', "", titulo_sem_pontuacao).replace(" ", "_")
                    # Formata o título para uso como identificador, substituindo espaços por underline.

            titulo_formatado_semespaco = titulo_formatado_semespaco.replace("º", "o")
            titulo_formatado_semespaco = titulo_formatado_semespaco.replace("ª", "a")
                    # Substitui caracteres específicos para manter compatibilidade com sistemas de arquivos.

            titulo_truncado = titulo_formatado_semespaco[:200].lower()
                # Trunca o título para 200 caracteres em minúsculas.
                # Processa e salva as imagens, páginas HTML e categorização de forma semelhante.


            diretorio_imagens = settings.MEDIA_ROOT
                # Diretório absoluto para salvar as imagens da notícia.
            os.makedirs(diretorio_imagens, exist_ok=True)
                # Cria o diretório de imagens se ele ainda não existir.

        

            times = {
                "atletico_mg": ["atleticomg", "galo", 282],
                "athletico_pr": ["atleticopr", "athletico", "furacao", 293],
                "bahia": ["bahia", "esquadrao", "esquadrao de aco", 265],
                "botafogo": ["botafogo", "fogao", 263],
                "bragantino": ["bragantino", "red bull bragantino", "massa bruta", 314],
                "corinthians": ["corinthians", "timao", 264],
                "cruzeiro": ["cruzeiro", "raposa", 276],
                "cuiaba": ["cuiaba", "dourado", 280],
                "flamengo": ["flamengo", "fla", "urubu", 262],
                "fluminense": ["fluminense", "flu", "tricolor das laranjeiras", 266],
                "fortaleza": ["fortaleza", "leao do pici", 315],
                "goias": ["goias", "esmeraldino", 275],
                "gremio": ["gremio", "tricolor gaucho", "imortal", 267],
                "internacional": ["inter", "colorado", 271],
                "palmeiras": ["palmeiras", "verdao", 272],
                "santos": ["santos", "peixe", 277],
                "sao_paulo": ["sao paulo", "spfc", "tricolor paulista", 274],
                "vasco": ["vasco", "vascao", "gigante da colina", 268],
                "coritiba": ["coritiba", "coxa", 278],
                "america_mg": ["americamg", "coelho", 285],
            }     
                # Lista de times para verificar se algum time está relacionado à notícia.

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
                # Dicionário de cores dos times


            try:                
                data_publicacao = timezone.now()
                    #pega a data atual para salvar no banco
                autor_text = "Desconhecido"
                    #o autor permanece desconhecido caso nao seja encontrado na noticia
                try:
                    autor_element = driver.find_element(By.CLASS_NAME, 'content-author__name')
                    autor_text = autor_element.text
                except:
                    pass
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
                    # Cria ou atualiza a notícia e salva no banco de dados


                categorias_encontradas = []
                    # Procura por categorias na lista de times com base no título da notícia
                time_id = None
                    #o time_id permanece none se ele nao conseguir associar


                # Quebra o título em palavras para preservar a ordem
                palavras_titulo = titulo_sem_pontuacao.lower().split()

                # Itera sobre as palavras do título, priorizando a ordem natural do texto
                for palavra in palavras_titulo:
                    for clube, dados in times.items():
                        if palavra in dados[:-1]:  # Verifica se a palavra é um apelido do time
                            if not categorias_encontradas:  # Se nenhuma categoria foi registrada
                                categorias_encontradas.append(clube)
                                time_id = dados[-1]  # Atribui o ID do time correspondente
                                break  # Para de buscar após encontrar o primeiro time
                    if categorias_encontradas:  # Se já encontrou uma categoria, para de iterar
                        break

                print(Fore.BLUE + f"🔍 Categoria escolhida: {categorias_encontradas[0] if categorias_encontradas else 'Nenhuma'}", '\n')



                if len(categorias_encontradas) == 0:
                    print(Fore.YELLOW + "⚠️ Não foi possível relacionar nenhuma categoria!", '\n')
                    categoria, _ = Categoria.objects.get_or_create(nome_categoria='outros')
                    CategoriaNoticias.objects.get_or_create(noticia=noticia_modelo, categoria=categoria)
                else:
                    if categorias_encontradas:
                        for nome_categoria in categorias_encontradas:
                            categoria, _ = Categoria.objects.get_or_create(nome_categoria=nome_categoria)
                            CategoriaNoticias.objects.get_or_create(noticia=noticia_modelo, categoria=categoria)
                    print(Fore.GREEN + f"Notícia '{titulo_truncado}' associada com a categoria '{categoria.nome_categoria}'.", '\n')
            except Exception as e:
                print(Fore.YELLOW + "⚠️ Não foi possível relacionar nenhuma categoria!", '\n')
                

            novo_id_noticia = noticia_modelo.id  
                # Obtenha o ID gerado


            try:
                imagens_elementos = driver.find_elements(By.CSS_SELECTOR, "amp-img")
                    # Localiza todos os elementos de imagem na página com o seletor CSS "amp-img".
                imagem_urls = []
                    # Inicializa uma lista vazia para armazenar os URLs das imagens.


                for j, imagem_elemento in enumerate(imagens_elementos):
                        # Itera sobre cada elemento de imagem encontrado, com um índice `j` para diferenciar as imagens.
                    url_imagem = imagem_elemento.get_attribute("src")
                        # Obtém o atributo `src` de cada elemento de imagem, que contém o URL da imagem.


                    nome_arquivo_imagem = os.path.join(f'{diretorio_imagens}/noticias', f"n_{novo_id_noticia}_{j}.jpg")
                        # Define o caminho e nome do arquivo para salvar a imagem localmente, com base no ID da notícia e no índice.
                    resposta_imagem = requests.get(url_imagem, stream=True)
                        # Faz uma requisição HTTP para o URL da imagem e ativa o modo "stream" para download por partes.
                    resposta_imagem.raise_for_status()
                        # Verifica se a requisição foi bem-sucedida. Lança uma exceção caso haja algum erro (e.g., 404 ou 500).


                    with open(nome_arquivo_imagem, 'wb') as file:
                            # Abre um arquivo no modo "write binary" para salvar os dados da imagem.
                        for chunk in resposta_imagem.iter_content(1024):
                                # Faz o download da imagem em blocos de 1024 bytes para economizar memória.

                            file.write(chunk)
                                # Escreve cada bloco baixado no arquivo.


                    imagem_urls.append(nome_arquivo_imagem)
                        # Adiciona o caminho da imagem salva à lista `imagem_urls`.
                    print(Fore.GREEN + f"✅ Imagem {j} salva como {nome_arquivo_imagem}")
                        # Exibe uma mensagem indicando que a imagem foi salva com sucesso.

                    
                    nome_arquivo_thumb = os.path.join(f'{diretorio_imagens}/thumbs', f"thumb_n_{novo_id_noticia}.jpg")
                        # Redimensiona a imagem e salva no diretório de miniaturas (thumbs)
                        # Define o caminho e nome do arquivo para salvar a miniatura da imagem.


                    with Image.open(nome_arquivo_imagem) as img:
                            # Abre a imagem salva usando a biblioteca Pillow.

                        img.thumbnail((380, 215))
                            # Redimensiona a imagem para um tamanho máximo de 380x215 pixels, mantendo a proporção.
                        img.save(nome_arquivo_thumb, "JPEG")
                            # Salva a miniatura no formato JPEG no diretório definido.
                    print(Fore.GREEN + f"✅ Miniatura da imagem {j} salva como {nome_arquivo_thumb}")
                        # Exibe uma mensagem indicando que a miniatura foi salva com sucesso.
            except Exception as e:
                print(Fore.RED + f"Erro ao baixar as imagens: {e}")
                    # Exibe uma mensagem de erro caso qualquer exceção seja levantada durante o processo.

                        

            nome_arquivo = f"{titulo_truncado}.html"
            caminho_arquivo = os.path.join('trendfeeds/templates/html/noticias', nome_arquivo)
                # Define o nome do arquivo e o caminho para salvar o HTML da notícia.


            html_content = f"""
            <html>
                <article class="noticia-detalhada">
                    <h1 class="noticia-titulo mt-4">{title_text}</h1>
                    <p class="noticia-conteudo">{content_text}</p>
                </article>
            </html>
            """
                # Cria o conteúdo HTML para a notícia.
            
            
            with open(caminho_arquivo, 'w', encoding='utf-8') as file:
                file.write(html_content)
                # Salva o HTML da notícia no diretório especificado.

            print(Fore.GREEN + f"✅Arquivo HTML criado com sucesso: {caminho_arquivo}", '\n')
            criado = 'sim'
                # Marca a notícia como criada.

            second_title_formatado = re.sub(r'[\\/*?:"<>|]', "", title_text)
            main_content_formatado = formatar_texto(titulo_formatado_semespaco, imagens_elementos, novo_id_noticia)


            caminho_arquivo = os.path.join('trendfeeds/templates/html/noticias', nome_arquivo)
                # Atualiza o caminho do arquivo HTML da notícia.
           
           
            categoria_nome = categorias_encontradas[0] if categorias_encontradas else "Outros"
            cor_categoria = cores_times.get(categoria_nome, "#cccccc")  
                # Cor padrão caso não encontre o time


            categoria_template_dir = 'trendfeeds/templates/html/categorias'
                # Local para salvar as páginas de categoria


            os.makedirs(categoria_template_dir, exist_ok=True)
                # Cria o diretório de categorias se ele ainda não existir
            


            if categorias_encontradas:
                for nome_categoria in categorias_encontradas:
                    try:
                        categoria, _ = Categoria.objects.get_or_create(nome_categoria=nome_categoria)
                            # Cria ou obtém a categoria no banco de dados.


                        CategoriaNoticias.objects.get_or_create(noticia=noticia_modelo, categoria=categoria)
                            # Associa a notícia à categoria.


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
                        
                        
                        cor_categoria = cores_times.get(nome_categoria, "#cccccc")
                            # Define cor da categoria; se não encontrar, usa a cor padrão

                        nome_arquivo_categoria = os.path.join(categoria_template_dir, f'index_{nome_categoria}.html')
                            # Define o nome do arquivo HTML para a página da categoria.

                        categorias_encontradas = []
                        time_id = None

                     

                        if not os.path.exists(nome_arquivo_categoria):
                            # Verifica se o arquivo existe; caso contrário, cria a página
                            html_categoria_content = f"""
{{% extends "html/modelo_categoria.html" %}}
{{% load static %}}

{{% block title %}}{nome_categoria}{{% endblock title %}}
{{% block main_title %}}{nome_categoria}{{% endblock main_title %}}
{{% block cor_categoria %}}{cor_categoria}{{% endblock cor_categoria %}}
{{% block id_time %}}{time_id}{{% endblock id_time %}}

<div class="categoria-listagem">
    <h2>Últimas notícias sobre {nome_categoria}</h2>
    <p>Aqui você encontrará todas as notícias sobre {nome_categoria}.</p>
</div>
                            """
                        
                            with open(nome_arquivo_categoria, "w", encoding="utf-8") as file:
                                file.write(html_categoria_content)
                                # Salva o conteúdo da página de categoria no arquivo.
                            
                            print(Fore.GREEN + f"📂 Página da categoria '{nome_categoria}' criada com sucesso em: {nome_arquivo_categoria}")
                                # Exibe mensagem de sucesso para criação da página de categoria.
                        else:
                            print(Fore.YELLOW + f"⚠️ A página da categoria '{nome_categoria}' já existe. Não será criada novamente.")
                                # Notifica que a página já existe e não será recriada.

                    except Exception as e:
                        print(Fore.RED + f"❌ Erro ao criar a página da categoria '{nome_categoria}': {e}")
                            # Exibe mensagem de erro ao criar a página da categoria.
            else:
                print(Fore.RED + "⚠️ Nenhuma categoria encontrada! Atribuindo à categoria 'Outros'.", '\n', '\n')
                    # Exibe mensagem ao não encontrar categorias para a notícia.


            html_content = f"""
            
{{% extends "html/modelo.html" %}}
{{% load static %}}

{{% block title %}}{categoria_nome}{{% endblock title %}}
{{% block main_title %}}{categoria_nome}{{% endblock main_title %}}
{{% block second_title %}}{second_title_formatado}{{% endblock second_title %}}
{{% block main_content %}}{main_content_formatado}{{% endblock main_content %}}
{{% block cor_categoria %}}{cor_categoria}{{% endblock cor_categoria %}}

"""
                # Cria o conteúdo HTML para a notícia, referenciando o template principal.


            if criado == 'sim':
                contador += 1
                # Incrementa o contador se o arquivo foi criado.
            if contador == 340:
                break
                # Encerra o loop após processar 8 notícias.
                                

            with open(caminho_arquivo, "w", encoding="utf-8") as file:
                file.write(html_content)
                # Salva o conteúdo renderizado no HTML.
            driver.get(url_principal)
            time.sleep(2)
                # Retorna à página principal e aguarda o carregamento.

    finally:
        driver.quit()
            # Encerra o navegador, independentemente de o resultado do processamento.
        print(Fore.GREEN + "🛑 Navegador encerrado. Coleta finalizada.")
            # Exibe mensagem indicando que o navegador foi fechado.










def pegar_resumo(texto):
        # Divide o texto na primeira ocorrência de quebra de linha e retorna apenas a primeira parte.
    primeira_linha = texto.split('\n', 1)[0]
    return primeira_linha.strip()
        # Remove espaços em branco no início e no final da primeira linha antes de retornar.










def formatar_texto(arquivo_nome, imagens_elementos, novo_id_noticia):
    nome_arquivo = arquivo_nome
        # Define o nome do arquivo e o caminho para buscá-lo.
    file_path = os.path.join('trendfeeds', 'templates', 'html', 'noticias', f'{arquivo_nome}.html')
    

    if __verificar_caminho(arquivo_nome, file_path): 
        text = __captar_tag(file_path)
            # Se o arquivo existe, captura seu conteúdo.
    else:
        text = ""
            # Caso contrário, inicializa com texto vazio.


    if text:
        text = re.sub(r'<[^>]+>', '', text)
            # Remove todas as tags HTML do texto.
        print("✅ Tags HTML removidas do texto!")
        text = re.sub(r'\+ [^\n]+', '', text)
            # Remove frases que começam com "+" seguido por texto até o final da linha.

        
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
        )# Define um padrão para capturar linhas que começam e terminam com emojis.


        text = emoji_pattern.sub('', text)
            # Substitui linhas que começam e terminam com emojis por uma string vazia.
        text = re.sub(r'Assista:.*?\.', '', text)
            # Remove frases que começam com "Assista:" e terminam com ".".
        text = re.sub(r'^Veja.*também$', '', text, flags=re.MULTILINE)
            # Remove frases que começam com "Veja" e terminam com "também".
        print("✅ Texto formatado com remoção de emojis, 'Assista:' e 'Veja...também'.")


    
    text = __adicionar_imagens(text, imagens_elementos, novo_id_noticia)
        # Adiciona imagens ao texto formatado.
   

    paragrafos = __dividir_por_pontos_finais(text, 3)
        # Divide o texto em parágrafos com base nos pontos finais.


   
    text = __criar_html_com_paragrafos(paragrafos)
        # Converte os parágrafos em HTML.
    print("✅ Texto processado e convertido em HTML.")
    return text










def __verificar_caminho(arquivo_nome, file_path):
    print('-' * 10, '🔍 VERIFICANDO A EXISTÊNCIA DO ARQUIVO', '-' * 10, '\n')
    print(f"📄 Recebendo título: {arquivo_nome}")


    if os.path.exists(file_path):
            # Verifica se o arquivo existe no caminho especificado.
        print(Fore.GREEN + f"✅ Arquivo encontrado: {file_path}\n")
        print('-' * 30)
        return True
    else:
            # Retorna uma string vazia se o arquivo não existir.
        print(Fore.RED + f"❌ Arquivo não encontrado: {file_path}\n")
        print('-' * 30)
        return ""










def __captar_tag(file_path):
    text = ""
        # Inicializa uma string vazia para armazenar o conteúdo da tag <p>.


    with open(file_path, 'r', encoding='utf-8') as file:
            # Abre o arquivo HTML para leitura.
        p_content = file.read()
        print(f"📂 Arquivo lido com sucesso: {file_path}")


    soup = BeautifulSoup(p_content, 'lxml')
        # Usa BeautifulSoup para analisar o conteúdo HTML.
    p_tag = soup.find('p')
        # Busca a primeira tag <p> no HTML.


    if p_tag:
            # Se a tag <p> foi encontrada, armazena o texto.
        text = p_tag.get_text()
    else:
        print("⚠️ Nenhuma tag <p> encontrada no conteúdo.")
    return text










def __dividir_por_pontos_finais(texto, num_pontos_finais):
    img_tags = re.findall(r'<img.*?>', texto)
        # Substitui temporariamente as tags <img> por marcadores únicos.
    for i, tag in enumerate(img_tags):
        texto = texto.replace(tag, f"[[IMG_TAG_{i}]]")


    sentencas = texto.split('.')
        # Divide o texto em sentenças com base nos pontos finais.
    paragrafos = []
        # Lista que armazenará os parágrafos.


    for i in range(0, len(sentencas), num_pontos_finais):
            # Agrupa as sentenças em parágrafos de acordo com o limite especificado.
        paragrafo_atual = '. '.join(sentencas[i:i + num_pontos_finais]).strip() + '.'

        if "Foto:" in paragrafo_atual or paragrafo_atual.strip():
            paragrafos.append(paragrafo_atual)
                # Adiciona o parágrafo se ele não estiver vazio.


   
    for i, tag in enumerate(img_tags):
        paragrafos = [paragrafo.replace(f"[[IMG_TAG_{i}]]", tag) for paragrafo in paragrafos]
            # Restaura as tags <img> nos parágrafos processados.
    print(f"✅ Texto dividido em {len(paragrafos)} parágrafos.")
    return paragrafos










def __criar_html_com_paragrafos(paragrafos):
    html_content = ""
        # Inicializa uma string para armazenar o HTML final
    

    for paragrafo in paragrafos:
            # Itera sobre cada parágrafo e insere tags <p>
        html_content += f"<p class='noticia-conteudo'>{paragrafo}</p>\n"


    html_content = mark_safe(html_content)
        # Marca o conteúdo como seguro para renderização em HTML no Django  
        # Evita a conversão de tags HTML em texto plano
    return html_content  
        # Retorna o conteúdo HTML formatado
    









def __adicionar_imagens(text, image_names, noticia_id):
    lines = text.split('\n')
        # Divide o texto em linhas.


    new_text = []
    image_index = 0


    for line in lines:
        if "Foto:" in line and image_index < len(image_names):
                # Adiciona a imagem correspondente ao texto com "Foto:".
            img_tag = f'<div class="div-imagem"><img class="noticia-imagem" src="{{% get_media_prefix %}}noticias/n_{noticia_id}_{image_index}.jpg"></div>'
            new_line = f"{img_tag}<p class='foto-descricao'>{line}</p>"
            new_text.append(new_line)
            image_index += 1
        else:
            new_text.append(line)


    final_text = '\n'.join(new_text)
    print(f"✅ {image_index} imagens adicionadas ao texto.")
    return final_text









def iniciar_scheduler():
    print("⏰ Scheduler iniciado.")
        # Esta função é um placeholder que pode ser expandida futuramente.
    pass
