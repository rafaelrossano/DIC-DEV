import requests
from datetime import datetime

from policia_dic_bot import bot

# Função para obter o timestamp atual
def get_timestamp():
    return datetime.now().strftime("%H:%M:%S %d/%m/%Y")

def post_sell(nickname, patente, valor):
    print('Iniciando requisição...')

    url = 'https://dic.systemhb.net/api/venda/aplicar'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Token-Auth': 'ok2gZV49WVPbre4%5MXc2nWR@joQOd',
        'Cookie': 'SAS=t0c3r895c3bog01tb18ev5cg0g; xke=23832d371339119a7b58f9960e7a71fd',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    body = {
        'nickname': nickname,
        'patente': patente,
        'valor': valor
    }

    try:
        response = requests.post(url, headers=headers, data=body)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        log_vendas(nickname, patente, valor, response.status_code, get_timestamp())
    except Exception as e:
        print(f"Erro ao realizar a requisição: {e}")

# Função para logar as vendas
def log_vendas(nickname, patente, valor, status_code, timestamp):
    if status_code == 200:
        print(f"[{timestamp}] Request bem-sucedido. Nickname: {nickname}, Patente: {patente}, Valor: {valor}")
    elif status_code == 400:
        print(f"[{timestamp}] Erro: Patente inválida para {nickname}.")
    elif status_code == 500:
        print(f"[{timestamp}] Erro: Erro interno do servidor.")
    elif status_code == 403:
        print(f"[{timestamp}] Erro: Modo de emergência ativado.")
    else:
        print(f"[{timestamp}] Erro desconhecido: {status_code}")

# Execução do programa
print('Iniciando o programa...')
post_sell('RafaelGOficial', 2, 2)
