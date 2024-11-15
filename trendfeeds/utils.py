# utils.py
import requests
from django.conf import settings
from datetime import datetime


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



