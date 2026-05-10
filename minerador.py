import requests
import re

# --- CONFIGURAÇÕES DA SUA VPS ---
BASE_URL = "http://213.199.56.115"
TOKEN_BASEROW = "KFB2YupQfqQZj6kFDwO6NKaje07vd6DP"
ID_TABELA_CONTEUDOS = "1186"
ID_CATEGORIA_CANAIS = 22 # ID correspondente a 'Canais' na sua tabela 1190

def criar_canal_no_baserow(nome, link):
    """
    Cria uma nova linha na tabela 1186 da sua VPS.
    """
    url = f"{BASE_URL}/api/database/rows/table/{ID_TABELA_CONTEUDOS}/?user_field_names=true"
    headers = {
        "Authorization": f"Token {TOKEN_BASEROW}",
        "Content-Type": "application/json"
    }
    
    # Payload com a estrutura que o seu Baserow espera
    payload = {
        "Nome": nome,
        "Link": link,
        "Capa": "https://imgur.com/vHEx37U.png", # Capa padrão para TV
        "Categoria": [ID_CATEGORIA_CANAIS]      # Vincula ao ID 22 (Canais)
    }
    
    try:
        # Enviando para a VPS (timeout de 15s para garantir a conexão)
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        return r.status_code
    except Exception as e:
        print(f"[!] Erro ao enviar {nome}: {e}")
        return 500

def minerar():
    # Fontes globais de alta confiabilidade
    fontes = [
        "https://iptv-org.github.io/iptv/countries/br.m3u",
        "https://raw.githubusercontent.com/LITUATUI/IPTV/main/BR.m3u",
        "https://raw.githubusercontent.com/frizon/iptv-brazil/master/brazil.m3u"
    ]
    
    print(f"[*] Iniciando a construção da grade de canais na VPS...")
    canais_encontrados = []
    
    headers_req = {'User-Agent': 'Mozilla/5.0'}

    for url in fontes:
        try:
            print(f"[*] Escaneando: {url}")
            r = requests.get(url, headers=headers_req, timeout=20)
            if r.status_code == 200:
                # Regex para extrair Nome e Link m3u8
                matches = re.findall(r'#EXTINF:.*?,(.*?)\n(https?://.*?\.m3u8.*)', r.text)
                for nome, link in matches:
                    n_up = nome.upper().strip()
                    # Filtro de canais premium para sua grade
                    premium = ["SPORTV", "HBO", "PREMIERE", "ESPN", "DISCOVERY", "DISNEY", "NICK", "AXN", "TNT"]
                    if any(p in n_up for p in premium):
                        canais_encontrados.append((nome.strip(), link.strip()))
        except:
            continue

    # Remove duplicados para evitar canais repetidos no banco
    lista_final = list(set(canais_encontrados))
    print(f"[*] Total de canais premium prontos para criação: {len(lista_final)}")

    if lista_final:
        sucesso = 0
        # Vamos processar os primeiros 30 para popular sua tabela rapidamente
        for nome, link in lista_final[:30]:
            print(f"[*] Criando: {nome}...")
            status = criar_canal_no_baserow(nome, link)
            
            if status in [200, 201]:
                sucesso += 1
                print(f"[OK] {nome} adicionado!")
            else:
                print(f"[ERRO {status}] Falha ao criar {nome}.")
        
        print(f"\n[FIM] {sucesso} canais novos criados na tabela 1186 da sua VPS.")
    else:
        print("[!] Nenhum canal encontrado nas fontes. Tente rodar o Action novamente.")

if __name__ == "__main__":
    minerar()
