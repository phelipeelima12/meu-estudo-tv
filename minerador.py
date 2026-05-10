import requests
import re
import json

# --- CONFIGURAÇÕES DA SUA VPS ---
BASE_URL = "http://213.199.56.115"
TOKEN_BASEROW = "KFB2YupQfqQZj6kFDwO6NKaje07vd6DP"
ID_TABELA_CONTEUDOS = "1186"
ID_CATEGORIA_CANAIS = 22 

def enviar_vps(nome, link):
    # Usamos o parâmetro user_field_names=true para tentar usar Nome/Link/Capa
    url = f"{BASE_URL}/api/database/rows/table/{ID_TABELA_CONTEUDOS}/?user_field_names=true"
    headers = {
        "Authorization": f"Token {TOKEN_BASEROW}",
        "Content-Type": "application/json"
    }
    
    # Payload formatado para o seu PHFLIX
    payload = {
        "Nome": nome,
        "Link": link,
        "Capa": "https://imgur.com/vHEx37U.png",
        "Categoria": [ID_CATEGORIA_CANAIS]
    }
    
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=20)
        
        if r.status_code in [200, 201]:
            print(f"[OK] Canal Criado: {nome}")
            return True
        else:
            # Se der erro, ele vai imprimir exatamente o que a VPS respondeu
            print(f"[!] Erro {r.status_code} em {nome}: {r.text}")
            return False
    except Exception as e:
        print(f"[!] Erro de conexão com a VPS: {e}")
        return False

def minerar():
    # Fontes globais de reserva
    fontes = [
        "https://iptv-org.github.io/iptv/countries/br.m3u",
        "https://raw.githubusercontent.com/LITUATUI/IPTV/main/BR.m3u"
    ]
    
    print(f"[*] Iniciando Injeção de Dados na VPS: {BASE_URL}")
    canais = []

    for url in fontes:
        try:
            res = requests.get(url, timeout=25)
            if res.status_code == 200:
                # Captura Nome e Link
                matches = re.findall(r'#EXTINF:.*?,(.*?)\n(https?://.*?\.m3u8.*)', res.text)
                for n, l in matches:
                    n_up = n.upper()
                    # Filtro para garantir que pegamos os principais
                    if any(p in n_up for p in ["SPORTV", "HBO", "PREMIERE", "ESPN", "NICK", "DISNEY", "TV"]):
                        canais.append((n.strip(), l.strip()))
        except:
            continue

    lista_limpa = list(set(canais))
    print(f"[*] Canais prontos para subir: {len(lista_limpa)}")

    if lista_limpa:
        sucesso = 0
        # Tenta subir os primeiros 5 para validar a estrutura
        for nome, link in lista_limpa[:5]:
            if enviar_vps(nome, link):
                sucesso += 1
        
        print(f"\n[FIM] Relatório: {sucesso} canais inseridos com sucesso.")
    else:
        print("[!] Nenhuma fonte retornou dados. Verifique sua internet ou as URLs das fontes.")

if __name__ == "__main__":
    minerar()
