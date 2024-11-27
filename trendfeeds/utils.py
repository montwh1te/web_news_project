''' **BIBLIOTECAS DE TERCEIROS** '''
import requests
    # Para fazer requisições HTTP a APIs externas.


''' **IMPORTAÇÕES DO DJANGO** '''
from django.conf import settings
    # Para pegar a api key dentro do arquivo settings.


''' **FUNÇÕES DA API FUTEBOL** '''
def obter_tabela_brasileirao():
    url = "https://api.api-futebol.com.br/v1/campeonatos/10/tabela"  # ID 10 refere-se à Série A
    headers = {
        "Authorization": f"Bearer {settings.API_FUTEBOL_KEY}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao acessar a API: {response.status_code} - {response.text}")
    




def obter_proximos_jogos():
    # Define a URL da API onde os dados dos próximos jogos serão buscados.
    url = "https://api.api-futebol.com.br/v1/campeonatos/10/rodadas/35"  # Substitua '34' pela rodada desejada dinamicamente.

    # Define os cabeçalhos da requisição, incluindo o token de autenticação para a API.
    headers = {
        "Authorization": f"Bearer {settings.API_FUTEBOL_KEY}"  # Insere o token da API configurado no Django settings.
    }


    try:
        # Envia a requisição HTTP para buscar os dados da API.
        response = requests.get(url, headers=headers)

        # Verifica se a requisição foi bem-sucedida. Caso contrário, lança uma exceção.
        response.raise_for_status()

        # Retorna a lista de partidas da resposta JSON.
        return response.json().get('partidas', [])
    except requests.exceptions.RequestException as e:
        
        # Em caso de erro, exibe o erro no console e retorna uma lista vazia.
        print(f"Erro ao buscar próximos jogos: {e}")
        return []







def obter_jogos_um_time(time):
    """
    Obtém os próximos jogos de um time específico pelo nome.
    
    Args:
        time (str): Nome do time (ex: 'internacional', 'palmeiras').
    
    Returns:
        list: Lista de partidas do time.
    """
    
    TIMES_IDS = {
        "internacional": 44,
        "palmeiras": 56,
        "botafogo": 22,
        "fortaleza": 131,
        "flamengo": 18,
        "sao_paulo": 57,
        "cruzeiro": 37,
        "bahia": 68,
        "corinthians": 65,
        "atletico_mg": 30,
        "vasco": 23,
        "vitoria": 102,
        "athletico_pr": 185,
        "gremio": 45,
        "juventude": 43,
        "criciuma": 1,
        "bragantino": 64,
        "cuiaba": 204,
        "atletico_go": 98,
        "fluminense": 26,
        "athletico_pr": 26,



    }

    # Verifica se o time existe no mapeamento, caso contrário levanta um erro
    if time not in TIMES_IDS:
        raise ValueError(f"Time '{time}' não encontrado. Verifique os nomes disponíveis.")
    
    # Obtemos o ID do time usando o nome
    id_time = TIMES_IDS[time]

    # Verifica se os dados já estão no cache (cache pode ser um dicionário global, por exemplo)


    # Configurações da API
    headers = {"Authorization": f"Bearer {settings.API_FUTEBOL_KEY}"}
    url = "https://api.api-futebol.com.br/v1/campeonatos/10/rodadas/35"

    # Fazendo a requisição
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Erro ao consultar a API: {response.status_code} - {response.text}")

    dados = response.json()

    # Filtra os jogos do time
    partidas = [
    partida for partida in dados.get('partidas', [])
    if partida['time_mandante']['time_id'] == id_time or partida['time_visitante']['time_id'] == id_time
    ]

    # Armazena no cache (se não estiver lá)
    return partidas