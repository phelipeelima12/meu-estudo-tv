import requests
import re

# --- CONFIGURAÇÕES DA SUA VPS ---
BASE_URL = "http://213.199.56.115"
TOKEN_BASEROW = "KFB2YupQfqQZj6kFDwO6NKaje07vd6DP"
ID_TABELA_CONTEUDOS = "1186"
ID_CATEGORIA_CANAIS = 22 

def enviar_vps(nome, link):
    # user_field_names=true faz o Baserow entender os nomes das colunas em vez de IDs chatos
    url = f"{BASE_URL}/api/database/rows/table/{ID_TABELA_CONTEUDOS}/?user_field_names=true"
    headers = {
        "Authorization": f"Token {TOKEN_BASEROW}",
        "Content-Type": "application/json"
    }
    
    # PAYLOAD: Ajustado para "Link" conforme sua instrução direta
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
            # Se der erro, ele vai cuspir o motivo exato aqui
            print(f"[!] Erro {r.status_code} em {nome}: {r.text}")
            return False
    except Exception as e:
        print(f"[!] Falha de conexão: {e}")
        return False

def minerar():
    fontes = [
        "https://iptv-org.github.io/iptv/countries/br.m3u",
        "https://raw.githubusercontent.com/LITUATUI/IPTV/main/BR.m3u"
    ]
    
    print(f"[*] Minerando e enviando para a coluna 'Link' na VPS...")
    canais = []

    for url in fontes:
        try:
            res = requests.get(url, timeout=25)
            if res.status_code == 200:
                matches = re.findall(r'#EXTINF:.*?,(.*?)\n(https?://.*?\.m3u8.*)', res.text)
                for n, l in matches:
                    n_up = n.upper()
                    # Pegando os principais canais fechados
                    if any(p in n_up for p in ["SPORTV", "HBO", "PREMIERE", "ESPN", "NICK", "DISNEY", "TNT"]):
                        canais.append((n.strip(), l.strip()))
        except:
            continue

    lista_limpa = list(set(canais))
    
    if lista_limpa:
        print(f"[*] Encontrados: {len(lista_limpa)}. Iniciando upload...")
        sucesso = 0
        # Vamos tentar subir os primeiros 15
        for nome, link in lista_limpa[:15]:
            if enviar_vps(nome, link):
                sucesso += 1
        print(f"\n[FIM] {sucesso} canais novos na sua tabela 1186!")
    else:
        print("[!] Nenhum link premium encontrado. Verifique as fontes.")

if __name__ == "__main__":
    minerar()
