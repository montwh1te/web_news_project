import re
#O re permite encontrar padrões de texto complexos. Por exemplo, buscar números, palavras específicas, ou padrões de formatação (como e-mails, CEPs, etc.).Usamos la no titulo formatado

from selenium import webdriver
#o webdriver, você ganha acesso a diferentes "drivers" específicos para cada navegador (como Chrome, Firefox, Edge, etc.) e pode controlar o navegador por meio de comandos no código.

from selenium.webdriver.chrome.service import Service
#Service para definir o caminho do driver do chrome

from selenium.webdriver.common.by import By
#O by é usado quando vamos procurar o elemento html pela class, id...

from selenium.webdriver.support.ui import WebDriverWait
#O WebDriverWait é usado para dizer quanto tempo ele deve esperar para fazer determinada acao

from selenium.webdriver.support import expected_conditions as EC
#EC verificar se tal elemento esta presente no dom

import time
#Usamos no sleep para parar e processar o codigo

from bs4 import BeautifulSoup

from trendfeeds.models import Noticias
#Importa a classe notcia do models para salvar as informacoes nessa tabela(noticias)

from django.template.loader import render_to_string
#serve para o modelo.html saber oque colocar dentro do bloco, no caso(titulo e conteudo)

import os
#os.path.join adapta o caminho corretamente.

import django

# Define o caminho para o arquivo de configurações
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_news.settings')

# Configura o Django com base no arquivo settings.py
django.setup()

def coletar_noticias():
    
    service = Service('')  
    # caminho driver do google

    options = webdriver.ChromeOptions()
    # Esta linha cria uma instância de ChromeOptions, que permite definir opções personalizadas para o navegador Chrome.

    #       options.add_argument("--headless")                  # Executa o Chrome sem abrir a interface
    #       options.add_argument("--disable-gpu")               # Desabilita o uso de GPU (recomendado para alguns sistemas)
    #       options.add_argument("--window-size=1920,1080")     # Define o tamanho da janela

    driver = webdriver.Chrome(service=service, options=options)
    #Função: Esta linha inicializa o navegador Chrome, aplicando as configurações definidas em service e options.

    url_principal = 'https://ge.globo.com/'  
    # URL da página principal do GE

    processed_urls = set()  
    # Conjunto para armazenar URLs processadas e evitar duplicidade

    try:
        driver.get(url_principal)  
        #Acessa o url principal

        for i in range(10):  
        # Limitar a 10 notícias
    
            noticias = WebDriverWait(driver, 20).until(
                # erro no catching CORRIGIR
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'feed-post-body'))
                # Esse é um método utilizado com WebDriverWait para aguardar até que um elemento esteja presente no DOM, independentemente de estar visível.

                #Ele é aplicado ao nível do driver (navegador), o que significa que ele procura globalmente na página, sem restrição a um elemento específico.

                #Esse método é útil para casos em que o carregamento do elemento pode demorar (como o título principal da página), e você quer garantir que ele esteja disponível antes de prosseguir.
            )
            # Obtém as notícias da página
            
            noticia = noticias[i]
            # Seleciona a notícia atual
        
            try:
                tempo_real = noticia.find_element(By.CLASS_NAME, 'bstn-aovivo-label')
                # Verifica se a notícia possui o marcador "tempo real" (a class) que é um jogo ao vivo

                #Esse método é usado para procurar um elemento específico dentro de um contexto existente. No seu caso, noticia.find_element(...) procura o elemento dentro do elemento noticia.

                #find_element realiza a busca a partir de um elemento pai específico, ou seja, ele só pesquisa dentro do elemento noticia.

                #Isso é útil quando você quer restringir a busca ao escopo de um elemento específico (neste caso, uma notícia específica).
                print(f"Notícia {i+1} marcada como Tempo Real, pulando...")
                continue  
                # Pula essa notícia se for "tempo real"
            except:
                pass 
                # Se não tiver marcador, continua


            
            try:
                link_noticia = noticia.find_element(By.CLASS_NAME, 'feed-post-link').get_attribute('href')
                titulo_noticia = noticia.find_element(By.CSS_SELECTOR, 'a.feed-post-link p').text.strip()
                # Captura o link e o título da notícia
            except:
                print(f"Erro ao capturar link ou título da notícia {i+1}, pulando...")
                continue
            

        
            if "/video" in link_noticia:
                # Verifica se o link contém
                print(f"Notícia {i+1} contém algo no link, pulando...")
                continue 
                # Pula a notícia se o link contiver 

            if "/jogo" in link_noticia:
                print(f"Notícia {i+1} contém algo no link, pulando...")
                continue 

            if "/playlist" in link_noticia:
                print(f"Notícia {i+1} contém algo no link, pulando...")
                continue 
        
            if link_noticia in processed_urls:
                print(f"Notícia {i+1} já processada, pulando...")
                # Verifica se o link já foi processado
                continue
            else:
                processed_urls.add(link_noticia)
                # Adiciona o link ao conjunto de URLs processadas  


            print(f"Notícia {i+1}: {titulo_noticia}")
            print(f"Link: {link_noticia}")
            # printa o numero da ordem da noticia que ele pegou com o titulo e o link dela

            driver.get(link_noticia)
            # Acessa a página da notícia
        
        
            try:
                title_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'content-head__title'))
                )
                # Captura o título da página da notícia
                title_text = title_element.text
                # Pega somente o texto do titulo
            except:
                print(f"Erro ao capturar o título da notícia {i+1}, pulando...")
                driver.get(url_principal)
                time.sleep(2)
                # Essa linha faz uma pausa fixa de 2 segundos antes de seguir para a próxima linha de código.
                continue

        
            try:
                content_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'mc-body'))
                    # Pega a descricao da noticia
                )
                content_text = content_element.text
            except:
                print(f"Erro ao capturar o conteudo da notícia {i+1}, pulando...")
                driver.get(url_principal)
                time.sleep(2)
                # Essa linha faz uma pausa fixa de 2 segundos antes de seguir para a próxima linha de código.
                # Diferente do 'WebDriverWait(driver, 10)' que faz uma pausa direto no navegador
                continue 
        
            titulo_formatado_semespaco = re.sub(r'[\\/*?:"<>|]', "", title_text)
            titulo_formatado_semespaco = titulo_formatado_semespaco.replace(" ", "_")  # Já substitui os espaços por "_"

            # Arquivo HTML criado para transformação do texto
            nome_arquivo = f"{titulo_formatado_semespaco}.html"
            caminho_arquivo = os.path.join('trendfeeds/templates/html', nome_arquivo)
            html_content = f"""
            <html>
                <article class="noticia-detalhada">
                    <h1 class="noticia-titulo mt-4">{title_text}</h1>
                    <p class="noticia-conteudo">{content_text}</p>
                </article>
            </html>
            """
            
            # Salvar o conteúdo no arquivo HTML
            with open(caminho_arquivo, 'w', encoding='utf-8') as file:
                file.write(html_content)
            print(f"Arquivo HTML criado com sucesso: {caminho_arquivo}")
            
           
            titulo_formatado = re.sub(r'[\\/*?:"<>|]', "", title_text)
            content_text_formatado = formatar_texto(titulo_formatado_semespaco)

            # Arquivo HTML final já com o texto transformado
            nome_arquivo = f"{titulo_formatado_semespaco}.html"
            # Define o nome do arquivo HTML e o conteúdo HTML
            caminho_arquivo = os.path.join('trendfeeds/templates/html', nome_arquivo)
            html_content = render_to_string('html/modelo.html', {
                'title_text': titulo_formatado,
                'content_text': content_text_formatado
            })


            with open(caminho_arquivo, "w", encoding="utf-8") as file:
                file.write(html_content)
            #"w" (write): Abre o arquivo para escrita. Se o arquivo já existir, "w" sobrescreve o conteúdo existente. Se o arquivo não existir, ele será criado.

            #"a" (append): Abre o arquivo para acrescentar conteúdo no final. Se o arquivo não existir, ele será criado. O "a" é útil para adicionar conteúdo a um arquivo existente sem sobrescrever.

            #"r" (read): Abre o arquivo para leitura. O arquivo precisa existir; caso contrário, um erro será gerado.
            
            print(f"Arquivo HTML criado com sucesso: {nome_arquivo}")

            """
            # Salva no banco de dados
            Noticias.objects.create(
                titulo=titulo_formatado,
                descricao=content_text_formatado,
            ) """

            
            driver.get(url_principal)
            time.sleep(2)
            # Retorna à página principal e aguarda o carregamento

    finally:
        driver.quit()
        #Fecha todas as janelas e encerra o processo do Chrome iniciado pelo Selenium, liberando os recursos do sistema.
        
def formatar_texto(arquivo_nome):
    
    print(f"Recebendo título: {arquivo_nome}")
    nome_arquivo = arquivo_nome
    
    # Caminho para o arquivo HTML na pasta templates
    file_path = f'trendfeeds/templates/html/{nome_arquivo}.html'
    
    # Verificação se o arquivo existe
    if os.path.exists(file_path):
        print(f"Arquivo encontrado: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            p_content = file.read()
    else:
        print(f"Arquivo não encontrado: {file_path}")
        return ""
        
    # Parsear o conteúdo HTML com BeautifulSoup
    soup = BeautifulSoup(p_content, 'lxml')

    # Busca a primeira tag <p> (já que só há uma)
    p_tag = soup.find('p')

    # Atribui ao text o conteúdo da tag <p>
    if p_tag:
        text = p_tag.get_text()
        print(text)
    else:
        text = ""
        print("Não foi encontrada nenhuma tag <p> no conteúdo.")

    # Remove tags HTML (se existirem outras tags no conteúdo)
    text = re.sub(r'<[^>]+>', '', text)
    print(text)

    # Remove frases com "+" no início
    text = re.sub(r'\+ [^\n]+', '', text)  
    print(text)
    
    # Retorna o texto como valor da função
    return text

def iniciar_scheduler():
    pass