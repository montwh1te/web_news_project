import requests

def listar_ids_times(campeonato_id, chave_api):
    """
    Lista os IDs e nomes dos times participantes de um campeonato na API-Futebol.
    
    Args:
        campeonato_id (int): O ID do campeonato a ser consultado.
        chave_api (str): Chave de autenticação para a API-Futebol.
        
    Returns:
        dict: Um dicionário com os IDs e nomes dos times.
    """
    url = f"https://api.api-futebol.com.br/v1/campeonatos/{campeonato_id}/tabela"
    headers = {
        "Authorization": f"Bearer {chave_api}"
    }
    
    # Faz a requisição para o endpoint
    response = requests.get(url, headers=headers)
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        tabela = response.json()
        times = {}
        
        # Itera pelos times na tabela
        for equipe in tabela:
            time_id = equipe['time']['time_id']
            nome_time = equipe['time']['nome_popular']
            times[time_id] = nome_time
        
        # Exibe os IDs e nomes dos times
        for id_time, nome in times.items():
            print(f"ID: {id_time}, Nome: {nome}")
        
        return times
    else:
        print(f"Erro: {response.status_code}, {response.json().get('mensagem', 'Erro desconhecido')}")
        print(response.json())
        return None

# Exemplo de uso:
campeonato_id = 14 # Brasileiro Série A
chave_api = "live_4bb165998f3bbcfcbd93a9da3e13eb"  # Substitua pela sua chave
listar_ids_times(campeonato_id, chave_api)
