import requests
import re

# --- CONFIGURAÇÕES DA SUA VPS ---
BASE_URL = "http://213.199.56.115"
TOKEN_BASEROW = "KFB2YupQfqQZj6kFDwO6NKaje07vd6DP"
ID_TABELA_CONTEUDOS = "1186"
ID_TABELA_CATEGORIAS = "1190"

def adicionar_novo_canal(nome, link):
    """
    Cria uma linha do zero na sua tabela 1186.
    Configura Nome, Link, Capa e vincula à Categoria 1190.
    """
    url = f"{BASE_URL}/api/database/rows/table/{ID_TABELA_CONTEUDOS}/?user_field_names=true"
    headers = {
        "Authorization": f"Token {TOKEN_BASEROW}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "Nome": nome,
        "Link": link,
        "Capa": "https://imgur.com/vHEx37U.png", # Capa padrão para TV
        "Categoria": [int(ID_TABELA_CATEGORIAS)]  # Vincula à sua categoria de TV
    }
    
    try:
        # Timeout de 15s para dar tempo da sua VPS responder
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        return r.status_code
    except Exception as e:
        print(f"[!] Erro ao conectar na VPS: {e}")
        return 500

def minerar():
    # Fontes globais que o seu robô já sabe ler
    fontes = [
        "https://iptv-org.github.io/iptv/countries/br.m3u",
        "https://raw.githubusercontent.com/LITUATUI/IPTV/main/BR.m3u",
        "https://raw.githubusercontent.com/frizon/iptv/master/brazil.m3u"
    ]
    
    print(f"[*] Iniciando a criação da sua grade de canais na VPS...")
    canais_para_adicionar = []
    
    headers_browser = {'User-Agent': 'Mozilla/5.0'}

    for url in fontes:
        try:
            print(f"[*] Escaneando fonte: {url}")
            res = requests.get(url, headers=headers_browser, timeout=20)
            if res.status_code == 200:
                # O Regex extrai o Nome e o Link m3u8
                matches = re.findall(r'#EXTINF:.*?,(.*?)\n(https?://.*?\.m3u8.*)', res.text)
                for nome, link in matches:
                    n_up = nome.upper()
                    # Filtro para pegar apenas o "filé mignon" (Canais Premium)
                    premium = ["SPORTV", "HBO", "PREMIERE", "ESPN", "DISCOVERY", "DISNEY", "NICK", "AXN", "TNT"]
                    if any(p in n_up for p in premium):
                        canais_para_adicionar.append((nome.strip(), link.strip()))
        except Exception as e:
            print(f"[!] Falha ao ler fonte: {e}")

    # Remove duplicados para não criar canais repetidos
    lista_final = list(set(canais_para_adicionar))
    print(f"[*] Total de canais premium encontrados: {len(lista_final)}")

    if lista_final:
        sucesso = 0
        # Vamos adicionar os primeiros 40 canais encontrados
        for nome, link in lista_final[:40]:
            print(f"[*] Tentando adicionar: {nome}...")
            status = adicionar_novo_canal(nome, link)
            
            if status in [200, 201]:
                sucesso += 1
                print(f"[OK] {nome} criado com sucesso!")
            else:
                print(f"[ERRO {status}] Não foi possível criar o canal {nome}.")
        
        print(f"\n[FIM] Missão cumprida! {sucesso} canais novos adicionados à sua VPS.")
    else:
        print("[!] O robô não encontrou links premium nas fontes agora. Tente rodar novamente mais tarde.")

if __name__ == "__main__":
    minerar()
