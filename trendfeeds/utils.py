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
    """
    Obtém os próximos jogos disponíveis no campeonato.
    
    Returns:
        list: Lista de jogos disponíveis.
    """
    import requests

    # Configuração da API
    headers = {"Authorization": f"Bearer {settings.API_FUTEBOL_KEY}"}
    url = "https://api.api-futebol.com.br/v1/campeonatos/10/rodadas/37"

    try:
        # Fazendo a requisição
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Levanta exceções para códigos HTTP de erro
        dados = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar a API: {e}")
        return []  # Retorna uma lista vazia em caso de erro

    # Retorna as partidas disponíveis
    return dados.get('partidas', [])





def obter_jogos_um_time(time, rodadas):
    """
    Obtém os jogos de um time específico para múltiplas rodadas.
    
    Args:
        time (str): Nome do time (ex: 'internacional', 'palmeiras').
        rodadas (list): Lista de números das rodadas a serem consultadas (ex: [35, 36, 37]).
    
    Returns:
        list: Lista de partidas do time nas rodadas especificadas.
    """
    import requests

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
    }

    # Verifica se o time existe no mapeamento
    if time not in TIMES_IDS:
        return []  # Retorna uma lista vazia se o time não for encontrado

    id_time = TIMES_IDS[time]

    headers = {"Authorization": f"Bearer {settings.API_FUTEBOL_KEY}"}
    url_template = "https://api.api-futebol.com.br/v1/campeonatos/10/rodadas/{}"
    partidas_total = []

    for rodada in rodadas:
        url = url_template.format(rodada)
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            dados = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao consultar a API na rodada {rodada}: {e}")
            continue  # Pula para a próxima rodada em caso de erro

        # Filtra os jogos do time
        partidas = [
            partida for partida in dados.get('partidas', [])
            if partida['time_mandante']['time_id'] == id_time or partida['time_visitante']['time_id'] == id_time
        ]
        partidas_total.extend(partidas)

    return partidas_total
