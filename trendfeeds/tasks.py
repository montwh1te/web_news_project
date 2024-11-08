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

from trendfeeds.models import Noticias
# Importa a classe 'Noticias' do models do Django, o que permite salvar notícias em uma tabela do banco de dados.

from django.template.loader import render_to_string
# render_to_string é usado para renderizar templates do Django em uma string HTML, facilitando a geração de conteúdo dinâmico.

from django.utils.safestring import mark_safe
# mark_safe é usado para garantir que uma string seja tratada como HTML, evitando a conversão de tags em texto.
# ex: "<p>Esta é uma notícia <b>importante</b>.</p>"
# viraria com o mark_safe:  "&lt;p&gt;Esta é uma notícia &lt;b&gt;importante&lt;/b&gt;.&lt;/p&gt;"

import os
# O módulo 'os' oferece funções para interagir com o sistema operacional, como 'os.path.join' para manipulação de caminhos de arquivos.

import django
# O módulo 'django' é necessário para configurar o ambiente do Django fora do servidor padrão, permitindo manipulação de modelos e templates.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_news.settings')
# DJANGO_SETTINGS_MODULE = Define o caminho para o arquivo de configurações
# web_news.settings = Configura o Django para que ele use as configurações especificadas no arquivo 'web_news.settings'.
#DJANGO_SETTINGS_MODULE é o nome da variável de ambiente que o Django usa para localizar o arquivo de configurações do projeto. Quando você executa comandos Django (como python manage.py runserver), essa variável já está configurada. No entanto, para scripts independentes, você precisa configurá-la manualmente.

django.setup()
# Configura o Django com base no arquivo settings.py
# Inicializa o Django, tornando disponíveis suas funcionalidades para o script atual.

def coletar_noticias():
    
    service = Service('')  
    # Configura o Service para especificar o caminho do driver do Chrome.

    options = webdriver.ChromeOptions()
    # Instancia as opções do navegador Chrome, permitindo configurações adicionais.

    driver = webdriver.Chrome(service=service, options=options)
    # Inicializa o navegador Chrome com o Service e opções especificadas, abrindo o navegador para navegação automatizada.

    url_principal = 'https://ge.globo.com/'  
    # Define a URL da página principal do GE (Globo Esporte), onde as notícias serão coletadas.

    processed_urls = set()  
    # Define um conjunto vazio para armazenar URLs já processadas, evitando duplicatas.

    current_scroll_position = 0  
    # Variável que rastreia a posição atual de rolagem na página.

    scroll_increment = 300  
    # Define a quantidade de pixels para rolar a cada incremento.

    contador = 0  
    # Contador para rastrear o número de notícias processadas.

    try:
        driver.get(url_principal)  
        # Acessa a página inicial do GE no navegador.

        for i in range(30):  
            # Limita o loop para processar até 30 notícias, rolando a página quando necessário.
            
            criado = 'nao'  
            # Marca se um arquivo foi criado para controle no contador.

            time.sleep(2)
            # Pausa o código por 2 segundos para permitir o carregamento da página.

            current_scroll_position += scroll_increment
            # Incrementa a posição atual de rolagem pela quantidade especificada em scroll_increment.

            driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")
            # Rola a página para baixo para carregar mais conteúdo.

            time.sleep(2)
            # Pausa o código por 2 segundos para garantir o carregamento dos elementos após a rolagem.

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'feed-post-body'))
            )
            # Aguarda até que elementos com a classe 'feed-post-body' estejam presentes na página.

            noticias = driver.find_elements(By.CLASS_NAME, 'feed-post-body')
            # Coleta todos os elementos com a classe 'feed-post-body', que representam as notícias na página.

            #print(len(noticias))
            # Exibe o número de notícias coletadas na iteração atual para controle.

            noticia = noticias[i]
            # Seleciona a notícia atual com base no índice do loop.

            try:
                tempo_real = noticia.find_element(By.CLASS_NAME, 'bstn-aovivo-label')
                # Verifica se a notícia é ao vivo, marcada com a classe 'bstn-aovivo-label'.

                print(f"Notícia {i+1} marcada como Tempo Real, pulando...")
                # Mensagem para indicar que a notícia ao vivo foi ignorada.
                continue
            except:
                pass
                # Se a notícia não for ao vivo, passa para a próxima etapa.

            try:
                link_noticia = noticia.find_element(By.CLASS_NAME, 'feed-post-link').get_attribute('href')
                # Coleta o link da notícia.

                titulo_noticia = noticia.find_element(By.CSS_SELECTOR, 'a.feed-post-link p').text.strip()
                # Coleta o título da notícia e remove espaços extras.
            except:
                print(f"Erro ao capturar link ou título da notícia {i+1}, pulando...")
                # Caso ocorra erro na captura de link ou título, a notícia é ignorada.
                continue

            if any(substring in link_noticia for substring in ["/video", "/jogo", "/playlist"]):
                print(f"Notícia {i+1} contém um link que será ignorado.")
                # Ignora notícias com links que contenham "/video", "/jogo" ou "/playlist".
                continue

            if link_noticia in processed_urls:
                print(f"Notícia {i+1} já processada, pulando...")
                # Ignora notícias cujos links já foram processados.
                continue
            else:
                processed_urls.add(link_noticia)
                # Adiciona o link da notícia ao conjunto de URLs processadas.

            print(f"Notícia {i+1}: {titulo_noticia}")
            print(f"Link: {link_noticia}")
            # Exibe o número, título e link da notícia que está sendo processada.

            driver.get(link_noticia)
            # Acessa o link da notícia para coletar mais detalhes.

            try:
                title_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'content-head__title'))
                )
                # Aguarda e coleta o título completo da notícia.

                title_text = title_element.text
                # Armazena o texto do título para posterior processamento.
            except:
                print(f"Erro ao capturar o título da notícia {i+1}, pulando...")
                # Exibe mensagem de erro se o título não for encontrado.
                driver.get(url_principal)
                # Retorna à página principal caso ocorra um erro.
                time.sleep(2)
                continue

            try:
                # Aguarda e coleta o conteúdo principal da notícia
                content_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'mc-body'))
                )
                content_text = content_element.text

                # Lista das classes a serem removidas do conteúdo principal
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

                
                for class_name in classes_para_remover:
                    try:
                        elemento_para_remover = content_element.find_element(By.CLASS_NAME, class_name)
                        # Itera sobre cada classe e tenta remover o texto correspondente, se encontrado
                        content_text = content_text.replace(elemento_para_remover.text, "")
                    except:
                        pass  
                    # Continua se o elemento não for encontrado
                    
                try:
                    elemento_para_remover = content_element.find_element(By.CSS_SELECTOR, "time")
                except:
                    pass
            except:
                print(f"Erro ao capturar o conteúdo da notícia {i+1}, pulando...")
                driver.get(url_principal)
                time.sleep(2)
                continue

           

            titulo_formatado_semespaco = re.sub(r'[\\/*?:"<>|]', "", title_text).replace(" ", "_")
            # Formata o título removendo caracteres especiais e substituindo espaços por "_".

            seletor_css_imagem = "amp-img"
            # Define o seletor para identificar as imagens no HTML da notícia.

            diretorio_imagens = "./media/"
            # Define o diretório onde as imagens serão salvas.

            os.makedirs(diretorio_imagens, exist_ok=True)
            # Cria o diretório se ele não existir.

            nome_arquivo_imagem = os.path.join(diretorio_imagens, f"{titulo_formatado_semespaco}.jpg")
            # Define o nome do arquivo da imagem com base no título formatado.

            try:
                imagens_elementos = driver.find_elements(By.CSS_SELECTOR, seletor_css_imagem)
                # Coleta todos os elementos de imagem com o seletor CSS especificado.

                for i, imagem_elemento in enumerate(imagens_elementos):
                    url_imagem = imagem_elemento.get_attribute("src")
                    # Captura a URL da imagem.
                    
                    nome_arquivo_imagem = os.path.join(diretorio_imagens, f"{titulo_formatado_semespaco}_{i}.jpg")
                    # Define o nome do arquivo para salvar a imagem.

                    resposta_imagem = requests.get(url_imagem, stream=True)
                    # Baixa a imagem.

                    resposta_imagem.raise_for_status()
                    # Verifica se o download foi bem-sucedido.

                    with open(nome_arquivo_imagem, 'wb') as file:
                    #Essa linha abre (ou cria, se não existir) um arquivo para escrita binária ('wb') com o nome especificado em nome_arquivo_imagem.
                    #O modo 'wb' é importante para imagens e outros arquivos binários (como PDFs) porque garante que o conteúdo será escrito no formato binário correto, preservando a estrutura dos dados.

                        for chunk in resposta_imagem.iter_content(1024):
                            file.write(chunk)
                    print(f"Imagem {i} salva como {nome_arquivo_imagem}")

            except Exception as e:
                print(f"Erro ao baixar as imagens: {e}")

            nome_arquivo = f"{titulo_formatado_semespaco}.html"
            # Define o nome do arquivo HTML com base no título formatado.

            caminho_arquivo = os.path.join('trendfeeds/templates', nome_arquivo)
            # Define o caminho completo do arquivo HTML.

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

            titulo_formatado = re.sub(r'[\\/*?:"<>|]', "", title_text)
            content_text_formatado = formatar_texto(titulo_formatado_semespaco)
            # Formata o título e o conteúdo da notícia para exibição.

            caminho_arquivo = os.path.join('trendfeeds/templates', nome_arquivo)
            html_content = render_to_string('modelo.html', {
                'title_text': titulo_formatado,
                'content_text': content_text_formatado
            })
            # Renderiza o template 'modelo.html' com o conteúdo da notícia.

            if criado == 'sim':
                contador += 1
            # Incrementa o contador se o arquivo foi criado.

            if contador == 10:
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
        # Fecha o navegador e libera recursos.
    



def formatar_texto(arquivo_nome):
   
    nome_arquivo = arquivo_nome
    file_path = f'trendfeeds/templates/{nome_arquivo}.html'
     # Define o nome do arquivo e o caminho para buscá-lo
    
    if __verificar_caminho(arquivo_nome, file_path):
         # Verifica se o arquivo existe e captura o conteúdo se disponível
        text = __captar_tag(file_path)  
        # Captura o conteúdo da tag <p> no arquivo HTML
    else:
        text = ""  
        # Define o texto como vazio caso o arquivo não seja encontrado

    if text: 
        # Remove tags HTML e outras formatações indesejadas
        # Só executa se 'text' não for vazio
        text = re.sub(r'<[^>]+>', '', text) 
        # Remove todas as tags HTML presentes

    text = re.sub(r'\+ [^\n]+', '', text)  
    # Remove frases que começam com "+"

    paragrafos = __dividir_por_pontos_finais(text, 3)
    # Divide o texto em parágrafos de tamanho controlado
    
    text = __criar_html_com_paragrafos(paragrafos)
    # Converte os parágrafos formatados em HTML com tags <p>

    return text




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
        
        if paragrafo_atual.strip():
            # Adiciona o parágrafo formatado à lista final 
            paragrafos.append(paragrafo_atual)
             # Ignora parágrafos vazios
        paragrafo_atual = ""
        # Reseta para o próximo parágrafo  
    
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
    



def iniciar_scheduler():
    pass