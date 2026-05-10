import requests
import re

# --- DADOS DA SUA VPS ---
BASE_URL = "http://213.199.56.115"
TOKEN_BASEROW = "KFB2YupQfqQZj6kFDwO6NKaje07vd6DP"
ID_TABELA_CONTEUDOS = "1186"
ID_CATEGORIA_CANAIS = 22 # Categoria 'Canais'

def adicionar_na_vps(nome, link):
    url = f"{BASE_URL}/api/database/rows/table/{ID_TABELA_CONTEUDOS}/?user_field_names=true"
    headers = {
        "Authorization": f"Token {TOKEN_BASEROW}",
        "Content-Type": "application/json"
    }
    
    # PAYLOAD AJUSTADO: Verifique se esses nomes batem com as colunas da sua VPS
    payload = {
        "Nome": nome,
        "Link": link,
        "Capa": "https://imgur.com/vHEx37U.png",
        "Categoria": [ID_CATEGORIA_CANAIS]
    }
    
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        if r.status_code in [200, 201]:
            print(f"[OK] Adicionado: {nome}")
            return True
        else:
            # ISSO AQUI VAI NOS DIZER O ERRO REAL
            print(f"[!] VPS Recusou {nome}. Erro {r.status_code}: {r.text}")
            return False
    except Exception as e:
        print(f"[!] Falha de conexão com a VPS: {e}")
        return False

def minerar():
    # Fontes globais que o robô sabe ler
    fontes = [
        "https://iptv-org.github.io/iptv/countries/br.m3u",
        "https://raw.githubusercontent.com/LITUATUI/IPTV/main/BR.m3u"
    ]
    
    print(f"[*] Iniciando construtor na VPS: {BASE_URL}")
    encontrados = []
    
    for url in fontes:
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                matches = re.findall(r'#EXTINF:.*?,(.*?)\n(https?://.*?\.m3u8.*)', r.text)
                for nome, link in matches:
                    n_up = nome.upper()
                    # Filtro focado em canais de TV
                    if any(t in n_up for t in ["SPORTV", "HBO", "PREMIERE", "ESPN", "NICK", "DISNEY", "TV"]):
                        encontrados.append((nome.strip(), link.strip()))
        except:
            continue

    lista = list(set(encontrados))
    print(f"[*] Canais encontrados para subir: {len(lista)}")

    if lista:
        sucesso = 0
        # Tenta subir os primeiros 10 para diagnóstico
        for nome, link in lista[:10]:
            if adicionar_na_vps(nome, link):
                sucesso += 1
        
        print(f"\n[FIM] {sucesso} canais novos na sua VPS!")
    else:
        print("[!] O robô não achou links. Verifique as fontes.")

if __name__ == "__main__":
    minerar()
