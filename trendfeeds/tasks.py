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
                content_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'mc-body'))
                )
                # Aguarda e coleta o conteúdo principal da notícia.
                content_text = content_element.text
            except:
                print(f"Erro ao capturar o conteudo da notícia {i+1}, pulando...")
                # Exibe mensagem de erro caso o conteúdo não seja encontrado.
                driver.get(url_principal)
                # Retorna à página principal.
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
    print(f"Recebendo título: {arquivo_nome}")
    
    # Verificação se o arquivo existe
    if os.path.exists(file_path):
        print(f"Arquivo encontrado: {file_path}\n")
        print('-'*30)
        return True
    else:
        print(f"Arquivo não encontrado: {file_path}\n")
        print('-'*30)
        return ""
    



def __captar_tag(file_path):
    text = ""  # Valor padrão caso não encontre a tag <p>
    with open(file_path, 'r', encoding='utf-8') as file:
        p_content = file.read()
        print(f'Arquivo criado!({file_path})')
        
    # Parsear o conteúdo HTML com BeautifulSoup
    soup = BeautifulSoup(p_content, 'lxml')

    # Busca a primeira tag <p> (já que só há uma)
    p_tag = soup.find('p')

    # Atribui ao text o conteúdo da tag <p> se a tag for encontrada
    if p_tag:
        text = p_tag.get_text()
    else:
        print("Não foi encontrada nenhuma tag <p> no conteúdo.")
        
    return text




def __dividir_por_pontos_finais(texto, num_pontos_finais):
    # Divide o texto com base nos pontos finais
    sentencas = texto.split('.')
    paragrafo_atual = ""
    paragrafos = []
    
    for i in range(0, len(sentencas), num_pontos_finais):
        # Adiciona num_pontos sentenças ao parágrafo atual, mas verifica o limite da lista
        paragrafo_atual = '. '.join(sentencas[i:i + num_pontos_finais]).strip() + '.'
        
        # Adiciona o parágrafo ao resultado final, se não estiver vazio
        if paragrafo_atual.strip():
            paragrafos.append(paragrafo_atual)
        paragrafo_atual = ""  # Reseta para o próximo parágrafo
    
    return paragrafos




def __criar_html_com_paragrafos(paragrafos):
    
    html_content = ""
    
    # Cria as tags <p> para cada parágrafo
    for paragrafo in paragrafos:
        html_content += f"<p class='noticia-conteudo'>{paragrafo}</p>\n"
        
    # Quando for retornar ou renderizar o HTML no Django
    html_content = mark_safe(html_content) 
    
    return html_content
    



def iniciar_scheduler():
    pass