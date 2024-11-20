import requests
from django.conf import settings


# **FUNÇÕES DA API FUTEBOL**
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
    url = "https://api.api-futebol.com.br/v1/campeonatos/10/rodadas/34"  # Substitua '34' pela rodada desejada dinamicamente.

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




