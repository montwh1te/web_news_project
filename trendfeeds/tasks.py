import re
# O módulo 're' é usado para trabalhar com expressões regulares em Python, permitindo encontrar e manipular padrões específicos no texto.

import requests
# O módulo 'requests' é utilizado para realizar requisições HTTP, permitindo que o código baixe imagens e conteúdo da web.

from selenium import webdriver 
# Importa o webdriver do Selenium, que permite automatizar o controle de navegadores da web, como o Chrome e Firefox.

from selenium.webdriver.chrome.service import Service
# Service é usado para especificar o caminho do driver do navegador (Chrome neste caso) para controlar o Chrome.

from selenium.webdriver.common.by import By
# O 'By' é uma classe que permite localizar elementos na página web com diferentes métodos, como By.CLASS_NAME, By.ID, etc.

from selenium.webdriver.support.ui import WebDriverWait
# WebDriverWait é uma função que permite definir o tempo máximo que o Selenium deve aguardar para que um determinado elemento apareça.

from selenium.webdriver.support import expected_conditions as EC
# EC (expected_conditions) contém métodos para verificar a presença ou visibilidade de elementos no DOM, como EC.presence_of_element_located.

import time
# O módulo 'time' oferece funções relacionadas a tempo, como 'sleep', que permite pausas no código por um tempo especificado.

from bs4 import BeautifulSoup
# BeautifulSoup é uma biblioteca para análise de HTML, usada aqui para facilitar a extração de dados de arquivos HTML.

from trendfeeds.models import Noticias, Categoria, CategoriaNoticias
# Importa a classe 'Noticias' do models do Django, o que permite salvar notícias em uma tabela do banco de dados.

from django.template.loader import render_to_string
# render_to_string é usado para renderizar templates do Django em uma string HTML, facilitando a geração de conteúdo dinâmico.

from django.utils.safestring import mark_safe
# mark_safe é usado para garantir que uma string seja tratada como HTML, evitando a conversão de tags em texto.

from PIL import Image
# Importa a biblioteca Pillow para manipulação e redimensionamento de imagens

from colorama import Fore, Style, init
# 'colorama' ajuda a colorir as mensagens de saída do terminal, útil para distinguir avisos e erros ao processar notícias.

from django.utils import timezone
# O timezone fornece funcionalidades de data/hora relacionadas ao fuso horário do Django.

from django.core.files import File
# Import necessário para manipulação e salvamento de arquivos de mídia no banco de dados.

from django.db.models import Max
# Importa a funcao necessaria para encontrar o id mais alto na tabela

import unicodedata
# O módulo 'unicodedata' permite normalizar textos, como remover acentos e caracteres especiais de strings.

import os
# O módulo 'os' oferece funções para interagir com o sistema operacional, como 'os.path.join' para manipulação de caminhos de arquivos.

import django
# O módulo 'django' é necessário para configurar o ambiente do Django fora do servidor padrão, permitindo manipulação de modelos e templates.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_news.settings')
# DJANGO_SETTINGS_MODULE define o caminho para o arquivo de configurações.
# 'web_news.settings' configura o Django para que ele use as configurações especificadas no arquivo 'web_news.settings'.

django.setup()
# Inicializa o Django, tornando disponíveis suas funcionalidades para o script atual.

init(autoreset=True)
# Inicializa o colorama, que permite que o terminal redefina as cores após cada linha.

from django.conf import settings
# Import necessário para usar 'MEDIA_URL' nas referências de mídia.

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
                print(f"Erro: Índice {i} fora do alcance para a lista de notícias. Total disponível: {len(noticias)}")
                continue
                        
           

            try:
                tempo_real = noticia.find_element(By.CLASS_NAME, 'bstn-aovivo-label')
                print(Fore.YELLOW + f"Notícia {i+1} marcada como Tempo Real, pulando...")
                # Ignora notícias marcadas como "Tempo Real" e passa para a próxima.
                continue
            except:
                pass
            
            try:
                link_noticia = noticia.find_element(By.CLASS_NAME, 'feed-post-link').get_attribute('href')
                titulo_noticia = noticia.find_element(By.CSS_SELECTOR, 'a.feed-post-link p').text.strip()
                # Captura o link e o título da notícia.
            except:
                print(Fore.RED + f"Erro ao capturar link ou título da notícia {i+1}, pulando...")
                continue

            if any(substring in link_noticia for substring in ["/video", "/jogo", "/playlist"]) or link_noticia in processed_urls:
                print(Fore.CYAN + f"Notícia {i+1} contém um link que será ignorado.")
                # Ignora links que contenham "/video", "/jogo", ou "/playlist" e URLs já processadas.
                continue

            processed_urls.add(link_noticia)
            # Adiciona o link ao conjunto de URLs processadas.

            print(Fore.GREEN + f"Notícia {i+1}: {titulo_noticia}")
            print(Fore.BLUE + f"Link: {link_noticia}")
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
                print(Fore.RED + f"Erro ao capturar o título da notícia {i+1}, pulando...")
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
                print(Fore.GREEN + f"Preview da notícia: {preview_content}")
                # Exibe um resumo da notícia extraído do conteúdo principal.
            except:
                print(f"Erro ao capturar o conteúdo da notícia {i+1}, pulando...")
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
            


            titulo_truncado = titulo_formatado_semespaco[:200].lower()
            # Trunca o título para 200 caracteres em minúsculas.

            diretorio_imagens = settings.MEDIA_ROOT
            # Diretório absoluto para salvar as imagens da notícia.

            os.makedirs(diretorio_imagens, exist_ok=True)
            # Cria o diretório de imagens se ele ainda não existir.

            titulo_formatado = re.sub(r'[\\/*?:"<>|]', "", title_text)
            # Formata o título da notícia para uso futuro.

            times = {
        "atletico_mg": ["atleticomg", "galo"],
        "atletico_pr": ["atleticopr", "athletico", "furacao"],
        "bahia": ["bahia", "esquadrao", "esquadrao de aco"],
        "botafogo": ["botafogo", "fogao"],
        "bragantino": ["bragantino", "red bull bragantino", "massa bruta"],
        "corinthians": ["corinthians", "timao"],
        "cruzeiro": ["cruzeiro", "raposa"],
        "cuiaba": ["cuiaba", "dourado"],
        "flamengo": ["flamengo", "fla", "urubu"],
        "fluminense": ["fluminense", "flu", "tricolor das laranjeiras"],
        "fortaleza": ["fortaleza", "leao do pici"],
        "goias": ["goias", "esmeraldino"],
        "gremio": ["gremio", "tricolor gaucho", "imortal"],
        "internacional": ["inter", "colorado"],
        "palmeiras": ["palmeiras", "verdao"],
        "santos": ["santos", "peixe"],
        "sao_paulo": ["sao paulo", "spfc", "tricolor paulista"],
        "vasco": ["vasco", "vascao", "gigante da colina"],
        "coritiba": ["coritiba", "coxa"],
        "america_mg": ["americamg", "coelho"],
        "selecao": ["selecao", "selecao brasileira", "canario", "canarinho"]
                    }
            
            # Dicionário de cores dos times
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
        "selecao": "#FFCC29"            # Amarelo
}


            
            # Lista de times para verificar se algum time está relacionado à notícia.


            try:                
                data_publicacao = timezone.now()

                autor_text = "Desconhecido"
                try:
                    autor_element = driver.find_element(By.CLASS_NAME, 'content-author__name')
                    autor_text = autor_element.text
                except:
                    pass
                
                
                # Cria ou atualiza a notícia e salva as imagens no banco de dados
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
                
                
                
                categorias_encontradas = []
                # Procura por categorias na lista de times com base no título da notícia
                
                for clube, apelidos in times.items():
                    if any(apelido in titulo_sem_pontuacao.lower() for apelido in apelidos):
                        categorias_encontradas.append(clube)
                        
                print(f'Categorias encontradas: {categorias_encontradas}')
                
                if len(categorias_encontradas) == 0:
                    
                    print('Não foi possível relacionar nenhuma categoria!')
                    categoria, _ = Categoria.objects.get_or_create(nome_categoria='outros')
                    CategoriaNoticias.objects.get_or_create(noticia=noticia_modelo, categoria=categoria)
                    
                else:
                    
                    if categorias_encontradas:
                        for nome_categoria in categorias_encontradas:
                            categoria, _ = Categoria.objects.get_or_create(nome_categoria=nome_categoria)
                            CategoriaNoticias.objects.get_or_create(noticia=noticia_modelo, categoria=categoria)
                    
                    print(Fore.GREEN + f"Notícia '{titulo_truncado}' associada com a categoria '{categoria.nome_categoria}'.")

            except Exception as e:
                print(Fore.RED + f"Erro ao criar/atualizar a notícia: {e}")
                
            novo_id_noticia = noticia_modelo.id  # Obtenha o ID gerado

            try:
                imagens_elementos = driver.find_elements(By.CSS_SELECTOR, "amp-img")
                imagem_urls = []
                for j, imagem_elemento in enumerate(imagens_elementos):
                    url_imagem = imagem_elemento.get_attribute("src")
                    nome_arquivo_imagem = os.path.join(f'{diretorio_imagens}/noticias', f"n_{novo_id_noticia}_{j}.jpg")
                    resposta_imagem = requests.get(url_imagem, stream=True)
                    resposta_imagem.raise_for_status()

                    with open(nome_arquivo_imagem, 'wb') as file:
                        for chunk in resposta_imagem.iter_content(1024):
                            file.write(chunk)
                    imagem_urls.append(nome_arquivo_imagem)
                    print(Fore.GREEN + f"Imagem {j} salva como {nome_arquivo_imagem}")
                    
                    # Redimensiona a imagem e salva no diretório de miniaturas (thumbs)
                    nome_arquivo_thumb = os.path.join(f'{diretorio_imagens}/thumbs', f"thumb_n_{novo_id_noticia}.jpg")
                    with Image.open(nome_arquivo_imagem) as img:
                        img.thumbnail((380, 215))  # Define o tamanho da miniatura
                        img.save(nome_arquivo_thumb, "JPEG")  # Salva a miniatura como JPEG
                    
                    print(Fore.GREEN + f"Miniatura da imagem {j} salva como {nome_arquivo_thumb}")

            except Exception as e:
                print(Fore.RED + f"Erro ao baixar as imagens: {e}")
                
                
                
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

            print(f"Arquivo HTML criado com sucesso: {caminho_arquivo}")
            criado = 'sim'
            # Marca a notícia como criada.

            second_title_formatado = re.sub(r'[\\/*?:"<>|]', "", title_text)
            main_content_formatado = formatar_texto(titulo_formatado_semespaco, imagens_elementos, novo_id_noticia)

            caminho_arquivo = os.path.join('trendfeeds/templates/html/noticias', nome_arquivo)
            # Atualiza o caminho do arquivo HTML da notícia.
           
           
            categoria_nome = categorias_encontradas[0] if categorias_encontradas else "Outros"
            cor_categoria = cores_times.get(categoria_nome, "#cccccc")  # Cor padrão caso não encontre o time

           



            categoria_template_dir = 'trendfeeds/templates/html/categorias'
             # Local para salvar as páginas de categoria

            os.makedirs(categoria_template_dir, exist_ok=True)
            # Cria o diretório de categorias se ele ainda não existir
            

            if categorias_encontradas:
                for nome_categoria in categorias_encontradas:
                    try:
                        categoria, _ = Categoria.objects.get_or_create(nome_categoria=nome_categoria)
                        CategoriaNoticias.objects.get_or_create(noticia=noticia_modelo, categoria=categoria)


                        cores_times = {
                            "atletico_mg": "#000000",          # Preto
                            "atletico_pr": "#cc0000",          # Vermelho escuro
                            "bahia": "#0033cc",                # Azul escuro
                            "botafogo": "#000000",             # Preto
                            "bragantino": "#cc0000",           # Vermelho escuro
                            "corinthians": "#333333",          # Cinza escuro
                            "cruzeiro": "#003399",             # Azul
                            "cuiaba": "#009933",               # Verde
                            "flamengo": "#ff0000",             # Vermelho
                            "fluminense": "#990000",           # Bordô
                            "fortaleza": "#003399",            # Azul
                            "goias": "#009933",                # Verde
                            "gremio": "#0066cc",               # Azul claro
                            "internacional": "#cc0000",        # Vermelho escuro
                            "palmeiras": "#006633",            # Verde escuro
                            "santos": "#000000",               # Preto
                            "sao_paulo": "#cc0000",            # Vermelho escuro
                            "vasco": "#000000",                # Preto
                            "coritiba": "#009933",             # Verde
                            "america_mg": "#009933",           # Verde
                            "selecao": "#ffcc00"               # Amarelo
                        }
                        
                        # Define cor da categoria; se não encontrar, usa a cor padrão
                        cor_categoria = cores_times.get(nome_categoria, "#cccccc")
                        
                        # Nome do arquivo da página de índice da categoria
                        nome_arquivo_categoria = os.path.join(categoria_template_dir, f'index_{nome_categoria}.html')
                        
                        # Verifica se o arquivo existe; caso contrário, cria a página
                        if not os.path.exists(nome_arquivo_categoria):
                            html_categoria_content = f"""
{{% extends "html/modelo_categoria.html" %}}
{{% load static %}}

{{% block title %}}{nome_categoria} - Notícias{{% endblock title %}}
{{% block main_title %}}{nome_categoria} - Notícias{{% endblock main_title %}}
{{% block cor_categoria %}}{cor_categoria}{{% endblock cor_categoria %}}

<div class="categoria-listagem">
    <h2>Últimas notícias sobre {nome_categoria}</h2>
    <p>Aqui você encontrará todas as notícias sobre {nome_categoria}.</p>
</div>
                            """
                            # Salva o arquivo HTML da categoria
                            with open(nome_arquivo_categoria, "w", encoding="utf-8") as file:
                                file.write(html_categoria_content)
                            
                            print(f"Página da categoria '{nome_categoria}' criada com sucesso em: {nome_arquivo_categoria}")
                        else:
                            print(f"A página da categoria '{nome_categoria}' já existe. Não será criada novamente.")

                    except Exception as e:
                        print(f"Erro ao criar a página da categoria '{nome_categoria}': {e}")
            else:
                # Se nenhuma categoria foi encontrada, atribui a categoria "Outros"
                print('Erro')






            html_content = f"""
            
{{% extends "html/modelo.html" %}}
{{% load static %}}

{{% block title %}}{categoria_nome}{{% endblock title %}}
{{% block main_title %}}{categoria_nome}{{% endblock main_title %}}
{{% block second_title %}}{second_title_formatado}{{% endblock second_title %}}
{{% block main_content %}}{main_content_formatado}{{% endblock main_content %}}
{{% block cor_categoria %}}{cor_categoria}{{% endblock cor_categoria %}}

"""
            # Renderiza o template 'modelo.html' com o conteúdo da notícia.

            # Pega o "modelo.html" como base para desenvolvimento dos novos html's.

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
        # Encerra o navegador, independentemente de o processo ter sido bem-sucedido.



def pegar_resumo(texto):
    # Divide o texto na primeira ocorrência de quebra de linha e retorna apenas a primeira parte
    primeira_linha = texto.split('\n', 1)[0]
    return primeira_linha.strip()



def formatar_texto(arquivo_nome, imagens_elementos, novo_id_noticia):
    nome_arquivo = arquivo_nome
    file_path = os.path.join('trendfeeds', 'templates', 'html', 'noticias', f'{arquivo_nome}.html')
    # Define o nome do arquivo e o caminho para buscá-lo
    
    if __verificar_caminho(arquivo_nome, file_path):
        text = __captar_tag(file_path)
    else:
        text = ""
    # Verifica se o arquivo existe e captura o conteúdo se disponível
    
    if text:
        # Remove todas as tags HTML
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove frases que começam com "+" seguido por texto até o final da linha
        text = re.sub(r'\+ [^\n]+', '', text)

        # Define um padrão para capturar linhas que começam e terminam com emojis
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

        # Substitui linhas que começam e terminam com emojis por uma string vazia
        text = emoji_pattern.sub('', text)

        text = re.sub(r'Assista:.*?\.', '', text)
        # Remove frases que começam com "Assista:" e terminam com "."


        # Remove frases que começam com "Veja" e terminam com "também"
        text = re.sub(r'^Veja.*também$', '', text, flags=re.MULTILINE)

        

    # Remove tags HTML, formatações indesejadas e frases com emojis e "Veja...também".
    
    text = __adicionar_imagens(text, imagens_elementos, novo_id_noticia)
    paragrafos = __dividir_por_pontos_finais(text, 3)
    text = __criar_html_com_paragrafos(paragrafos)
    return text
    # Adiciona imagens, divide o texto em parágrafos e converte em HTML.



def __verificar_caminho(arquivo_nome, file_path):
   
    print('-'*10,'VERIFICANDO A EXISTÊNCIA DO ARQUIVO','-'*10,'\n')
    # Exibe uma mensagem de verificação do arquivo
    print(f"Recebendo título: {arquivo_nome}")
    
    if os.path.exists(file_path):
        # Verifica se o arquivo existe no caminho especificado
        print(f"Arquivo encontrado: {file_path}\n")
        print('-'*30)
        return True  
        # Retorna True se o arquivo existir
    else:
        print(f"Arquivo não encontrado: {file_path}\n")
        print('-'*30)
        return ""  
        # Retorna uma string vazia se o arquivo não existir




def __captar_tag(file_path):
   
    text = ""
    # Define uma string vazia para armazenar o conteúdo da tag <p>
    
    with open(file_path, 'r', encoding='utf-8') as file:
        # Abre o arquivo HTML para leitura
        p_content = file.read()  
        # Lê o conteúdo do arquivo
        print(f'Arquivo criado!({file_path})')  
        # Indica que o arquivo foi lido
        
    soup = BeautifulSoup(p_content, 'lxml')
    # Usa BeautifulSoup para analisar o conteúdo HTML

    p_tag = soup.find('p')
    # Busca a primeira tag <p> no HTML

    if p_tag:
        # Se a tag <p> foi encontrada, armazena o texto
        text = p_tag.get_text()  
        # Extrai o texto da tag <p>
    else:
        print("Não foi encontrada nenhuma tag <p> no conteúdo.")  
        # Indica que a tag <p> está ausente

    return text  
    # Retorna o texto extraído




def __dividir_por_pontos_finais(texto, num_pontos_finais):

    img_tags = re.findall(r'<img.*?>', texto)
    # Substitui as tags <img> temporariamente por um marcador único sem pontos.
    for i, tag in enumerate(img_tags):
        texto = texto.replace(tag, f"[[IMG_TAG_{i}]]")

    sentencas = texto.split('.')
    # Divide o texto em sentenças com base nos pontos finais (.)
    paragrafo_atual = ""  
    # Armazena as sentenças temporárias para formar parágrafos
    paragrafos = []  
    # Lista que armazenará parágrafos completos
    
    for i in range(0, len(sentencas), num_pontos_finais):
    # Itera através das sentenças agrupando-as em parágrafos
        
        paragrafo_atual = '. '.join(sentencas[i:i + num_pontos_finais]).strip() + '.'
        # Junta as sentenças no limite especificado (num_pontos_finais)
        
        if "Foto:" in paragrafo_atual:
            paragrafos.append(paragrafo_atual)  # Adiciona o parágrafo
            paragrafo_atual = ""  # Reseta para o próximo parágrafo
        elif paragrafo_atual.strip():
            # Adiciona o parágrafo formatado à lista final
            paragrafos.append(paragrafo_atual)
             
        paragrafo_atual = ""
        # Reseta para o próximo parágrafo  
        
    # Junta os parágrafos de volta em uma string
    for i, tag in enumerate(img_tags):
        paragrafos = [paragrafo.replace(f"[[IMG_TAG_{i}]]", tag) for paragrafo in paragrafos]
    # Restaura as tags <img> substituindo os marcadores originais.


        
    return paragrafos 
    # Retorna a lista de parágrafos




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
    new_text = []
    image_index = 0

    for line in lines:
        # Ajuste para inserir a tag <img> com `MEDIA_URL`
        if "Foto:" in line and image_index < len(image_names):
            img_tag = f'<div class="div-imagem"><img class="noticia-imagem" src="{{% get_media_prefix %}}noticias/n_{noticia_id}_{image_index}.jpg"></div>'
            new_line = f"{img_tag}<p class='foto-descricao'>{line}</p>"
            new_text.append(new_line)
            image_index += 1
        else:
            new_text.append(line)  # Adiciona as linhas sem "Foto:"

    final_text = '\n'.join(new_text)
    return final_text




def iniciar_scheduler():
    pass