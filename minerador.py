import requests
import re

# --- CONFIGURAÇÕES DA SUA VPS ---
BASE_URL = "http://213.199.56.115"
TOKEN_BASEROW = "KFB2YupQfqQZj6kFDwO6NKaje07vd6DP"
ID_TABELA_CONTEUDOS = "1186"
ID_CATEGORIA_CANAIS = 22 

def enviar_vps(nome, link):
    url = f"{BASE_URL}/api/database/rows/table/{ID_TABELA_CONTEUDOS}/?user_field_names=true"
    headers = {
        "Authorization": f"Token {TOKEN_BASEROW}",
        "Content-Type": "application/json"
    }
    
    # REMOVI O CAMPO "Capa" PARA EVITAR O ERRO 400
    payload = {
        "Nome": nome,
        "Link": link,
        "Categoria": [ID_CATEGORIA_CANAIS]
    }
    
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=20)
        
        if r.status_code in [200, 201]:
            print(f"[OK] Canal Criado: {nome}")
            return True
        else:
            # Se ainda der erro, o log vai nos dizer qual campo sobrou que está errado
            print(f"[!] Erro {r.status_code} em {nome}: {r.text}")
            return False
    except Exception as e:
        print(f"[!] Erro de conexão com a VPS: {e}")
        return False

def minerar():
    fontes = [
        "https://iptv-org.github.io/iptv/countries/br.m3u",
        "https://raw.githubusercontent.com/LITUATUI/IPTV/main/BR.m3u"
    ]
    
    print(f"[*] Iniciando Injeção Direta na VPS: {BASE_URL}")
    canais = []

    for url in fontes:
        try:
            res = requests.get(url, timeout=25)
            if res.status_code == 200:
                matches = re.findall(r'#EXTINF:.*?,(.*?)\n(https?://.*?\.m3u8.*)', res.text)
                for n, l in matches:
                    n_up = n.upper()
                    # Filtro para os principais canais
                    if any(p in n_up for p in ["SPORTV", "HBO", "PREMIERE", "ESPN", "NICK", "DISNEY"]):
                        canais.append((n.strip(), l.strip()))
        except:
            continue

    lista_limpa = list(set(canais))
    
    if lista_limpa:
        print(f"[*] Canais encontrados: {len(lista_limpa)}. Tentando subir os 5 primeiros...")
        sucesso = 0
        for nome, link in lista_limpa[:5]:
            if enviar_vps(nome, link):
                sucesso += 1
        print(f"\n[FIM] Sucesso: {sucesso} canais inseridos.")
    else:
        print("[!] Nenhum canal encontrado nas fontes.")

if __name__ == "__main__":
    minerar()
