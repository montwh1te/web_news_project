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

from trendfeeds.models import Noticias, CategoriaNoticias, ImagemNoticias
# Importa a classe 'Noticias' do models do Django, o que permite salvar notícias em uma tabela do banco de dados.

from django.template.loader import render_to_string
# render_to_string é usado para renderizar templates do Django em uma string HTML, facilitando a geração de conteúdo dinâmico.

from django.utils.safestring import mark_safe
# mark_safe é usado para garantir que uma string seja tratada como HTML, evitando a conversão de tags em texto.
# ex: "<p>Esta é uma notícia <b>importante</b>.</p>"
# viraria com o mark_safe:  "&lt;p&gt;Esta é uma notícia &lt;b&gt;importante&lt;/b&gt;.&lt;/p&gt;"

from colorama import Fore, Style, init

from django.utils import timezone

from django.core.files import File  # Import necessário para manipulação de arquivos

import unicodedata

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

# Inicializa o colorama
init(autoreset=True)

from django.core.files import File  # Import necessário para manipulação de arquivos
driver = None

def coletar_noticias():
    service = Service('')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    url_principal = 'https://ge.globo.com/'
    processed_urls = set()
    current_scroll_position = 0
    scroll_increment = 550
    contador = 0

    try:
        driver.get(url_principal)

        for i in range(30):
            criado = 'nao'
            time.sleep(2)
            current_scroll_position += scroll_increment
            driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")
            time.sleep(2)

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'feed-post-body'))
            )

            noticias = driver.find_elements(By.CLASS_NAME, 'feed-post-body')
            #print(len(noticias))

            noticia = noticias[i]

            try:
                tempo_real = noticia.find_element(By.CLASS_NAME, 'bstn-aovivo-label')
                print(Fore.YELLOW + f"Notícia {i+1} marcada como Tempo Real, pulando...")
                continue
            except:
                pass

            try:
                link_noticia = noticia.find_element(By.CLASS_NAME, 'feed-post-link').get_attribute('href')
                titulo_noticia = noticia.find_element(By.CSS_SELECTOR, 'a.feed-post-link p').text.strip()
            except:
                print(Fore.RED + f"Erro ao capturar link ou título da notícia {i+1}, pulando...")
                continue

            if any(substring in link_noticia for substring in ["/video", "/jogo", "/playlist"]) or link_noticia in processed_urls:
                print(Fore.CYAN + f"Notícia {i+1} contém um link que será ignorado.")
                continue

            processed_urls.add(link_noticia)
            print(Fore.GREEN + f"Notícia {i+1}: {titulo_noticia}")
            print(Fore.BLUE + f"Link: {link_noticia}")

            driver.get(link_noticia)


            try:
                title_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'content-head__title'))
                )
                title_text = title_element.text
            except:
                print(Fore.RED + f"Erro ao capturar o título da notícia {i+1}, pulando...")
                driver.get(url_principal)
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

                preview_content = pegar_resumo(content_text)
                print(Fore.GREEN + f"Preview da notícia: {preview_content}")
            except:
                print(f"Erro ao capturar o conteúdo da notícia {i+1}, pulando...")
                driver.get(url_principal)
                time.sleep(2)
                continue

            titulo_normalizado = unicodedata.normalize('NFD', title_text)
         
            titulo_sem_acento = ''.join([c for c in titulo_normalizado if unicodedata.category(c) != 'Mn'])
            
            titulo_sem_pontuacao = re.sub(r'[{}%@#$%^&*()!<>:"/\\|+_=,.?;^~`-]', '', titulo_sem_acento)

            titulo_formatado_semespaco = re.sub(r'[\\/*?:"<>|]', "", titulo_sem_pontuacao).replace(" ", "_")

           

            titulo_truncado = titulo_formatado_semespaco[:200].lower()
            diretorio_imagens = "./media/"
            os.makedirs(diretorio_imagens, exist_ok=True)

            try:
                imagens_elementos = driver.find_elements(By.CSS_SELECTOR, "amp-img")
                imagem_urls = []
                for j, imagem_elemento in enumerate(imagens_elementos):
                    url_imagem = imagem_elemento.get_attribute("src")
                    nome_arquivo_imagem = os.path.join(diretorio_imagens, f"{titulo_truncado}_{j}.jpg")
                    resposta_imagem = requests.get(url_imagem, stream=True)
                    resposta_imagem.raise_for_status()
                    with open(nome_arquivo_imagem, 'wb') as file:
                        for chunk in resposta_imagem.iter_content(1024):
                            file.write(chunk)
                    imagem_urls.append(nome_arquivo_imagem)
                    print(Fore.GREEN + f"Imagem {j} salva como {nome_arquivo_imagem}")

            except Exception as e:
                print(Fore.RED + f"Erro ao baixar as imagens: {e}")

            titulo_formatado = re.sub(r'[\\/*?:"<>|]', "", title_text)

            times = [
                "flamengo", "palmeiras", "são paulo", "corinthians", "vasco da gama",
                "fluminense", "internacional", "grêmio", "cruzeiro", "atlético mineiro",
                "santos", "botafogo", "atlético paranaense", "sport recife", "bahia",
                "ceará", "fortaleza", "vitória", "chapecoense", "américa mineiro", "goiás",
                "avaí", "botafogo sp", "figueirense", "coritiba", "náutico", "ponte preta",
                "cuiabá", "bragantino"
            ]

            try:
                time_encontrado = None
                for clube in times:
                    if clube in titulo_formatado.lower():
                        time_encontrado = clube
                        time_encontrado = time_encontrado.strip().lower()
                        break

                if time_encontrado:
                    categoria, created = CategoriaNoticias.objects.get_or_create(nomecategoria=time_encontrado)
                else:
                    categoria, created = CategoriaNoticias.objects.get_or_create(nomecategoria="outro")

            except Exception as e:
                print(Fore.RED + f"Erro ao associar a categoria: {e}")

            data_publicacao = timezone.now()

            try:
                autor_element = driver.find_element(By.CLASS_NAME, 'content-author__name')
                autor_text = autor_element.text
            except:
                autor_text = "Desconhecido"

          

            nome_arquivo = f"{titulo_truncado}.html"
            caminho_arquivo = os.path.join('trendfeeds/templates/html/noticias', nome_arquivo)
           

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
            content_text_formatado = formatar_texto(titulo_formatado_semespaco, imagens_elementos, titulo_formatado_semespaco)
            # Formata o título e o conteúdo da notícia para exibição.

            caminho_arquivo = os.path.join('trendfeeds/templates/html/noticias', nome_arquivo)
            html_content = render_to_string('html/modelo.html', {
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

            try:
                noticia_modelo, created = Noticias.objects.update_or_create(
                    titulo=titulo_truncado,
                    defaults={
                        'data_publicacao': data_publicacao,
                        'descricao': preview_content,
                        'autor': autor_text,
                        'categoria': categoria,
                        'link':link_noticia
                    }
                )
                print(Fore.GREEN + f"Notícia '{titulo_truncado}' {'criada' if created else 'atualizada'} no banco de dados com sucesso.")

                # Limpa as imagens e insere novamente no banco de dados
                ImagemNoticias.objects.filter(noticia=noticia_modelo).delete()
                for imagem_url in imagem_urls:
                    with open(imagem_url, 'rb') as img_file:
                        ImagemNoticias.objects.create(noticia=noticia_modelo, imagem=File(img_file))

            except Exception as e:
                print(Fore.RED + f"Erro ao criar/atualizar a notícia: {e}")

           

            with open(caminho_arquivo, "w", encoding="utf-8") as file:
                file.write(html_content)
            # Salva o conteúdo renderizado no HTML.

            driver.get(url_principal)
            time.sleep(2)
            # Retorna à página principal e aguarda o carregamento.

    finally:
        driver.quit()


# Função para extrair as 3 primeiras frases
def pegar_resumo(content_text, num_frases=3):
    # Divide o conteúdo em frases com base no ponto final
    frases = content_text.split('.')
    # Retorna as primeiras 'num_frases' frases
    return '. '.join(frases[:num_frases]) + ('.' if len(frases) > num_frases else '')


def formatar_texto(arquivo_nome, imagens_elementos, titulo_formatado_semespaco):
   
    nome_arquivo = arquivo_nome
    file_path = f'trendfeeds/templates/html/noticias/{nome_arquivo}.html'
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
        
        # Remove frases que começam com qualquer emoji
        emoji_pattern = re.compile(
            r'^[\U0001F600-\U0001F64F]'  # Emojis de carinhas
            r'|^[\U0001F300-\U0001F5FF]'  # Símbolos e pictogramas diversos
            r'|^[\U0001F680-\U0001F6FF]'  # Símbolos de transporte e mapas
            r'|^[\U0001F700-\U0001F77F]'  # Símbolos alquímicos
            r'|^[\U0001F780-\U0001F7FF]'  # Símbolos geométricos adicionais
            r'|^[\U0001F800-\U0001F8FF]'  # Símbolos de seta suplementares
            r'|^[\U0001F900-\U0001F9FF]'  # Emojis de mão, gestos e pessoas
            r'|^[\U0001FA00-\U0001FA6F]'  # Objetos variados
            r'|^[\U0001FA70-\U0001FAFF]'  # Emojis de símbolos adicionais
            r'|^[\U00002700-\U000027BF]'  # Dingbats
            r'|^[\U0001F1E0-\U0001F1FF]'  # Bandeiras de países
            , flags=re.MULTILINE
        )

        # Aplica o padrão ao texto para remover linhas que começam com qualquer emoji
        text = emoji_pattern.sub('', text)
        
        text = re.sub(r'^Veja.*também$', '', text, flags=re.MULTILINE)
        # Remove frases que começam com "Veja" e terminam com "também"
    
    text = __adicionar_imagens(text, imagens_elementos, titulo_formatado_semespaco)

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
    
    
def __adicionar_imagens(text, image_names, title):
    lines = text.split('\n')
    new_text = []
    image_index = 0

    # ARRUMAR AQUI DESCRICAO DE IMAGENS

    for line in lines:
        # Se encontrar uma linha com "Foto:", substitui a linha de forma a incluir a tag <img> dentro da mesma <p>
        if "Foto:" in line and image_index < len(image_names):
            # Tag <img> dentro da mesma <p> que a descrição
            img_tag = f'<div class="div-imagem"><img class="noticia-imagem" src="../media/{title}_{image_index}.jpg"></div>'
            new_line = f"{img_tag}{line}"
            new_text.append(new_line)
            image_index += 1
        else:
            new_text.append(line)  # Adiciona as linhas que não contêm "Foto:"
            
    final_text = '\n'.join(new_text)
    # Junta todas as linhas de volta em uma única string
    
    return final_text



def iniciar_scheduler():
    pass