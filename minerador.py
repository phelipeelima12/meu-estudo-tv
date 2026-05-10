import requests
import re

# --- CONFIGURAÇÕES DA SUA VPS ---
BASE_URL = "http://213.199.56.115"
TOKEN_BASEROW = "KFB2YupQfqQZj6kFDwO6NKaje07vd6DP"
ID_TABELA_CONTEUDOS = "1186"
ID_TABELA_CATEGORIAS = "1190"

def limpar_canais_antigos():
    """
    Remove apenas os itens de TV da sua VPS na tabela 1186.
    Preserva Filmes e Séries.
    """
    print(f"[*] Conectando à VPS {BASE_URL} para limpeza seletiva...")
    url = f"{BASE_URL}/api/database/rows/table/{ID_TABELA_CONTEUDOS}/?user_field_names=true"
    headers = {"Authorization": f"Token {TOKEN_BASEROW}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            linhas = response.json().get("results", [])
            for linha in linhas:
                nome = str(linha.get("Nome", "")).upper()
                
                # Critério: apaga apenas canais premium conhecidos para atualizar o link
                if any(p in nome for p in ["SPORTV", "HBO", "PREMIERE", "ESPN", "DISCOVERY", "DISNEY", "NICK"]):
                    id_linha = linha["id"]
                    requests.delete(f"{BASE_URL}/api/database/rows/table/{ID_TABELA_CONTEUDOS}/{id_linha}/", headers=headers)
        print("[OK] Canais antigos removidos da VPS.")
    except Exception as e:
        print(f"[!] Erro na conexão com a VPS: {e}")

def subir_canais_novos(canais):
    """
    Envia os novos links para a tabela 1186 na sua VPS.
    """
    print(f"[*] Enviando {len(canais)} canais para a sua API na VPS...")
    url = f"{BASE_URL}/api/database/rows/table/{ID_TABELA_CONTEUDOS}/?user_field_names=true"
    headers = {
        "Authorization": f"Token {TOKEN_BASEROW}",
        "Content-Type": "application/json"
    }
    
    for nome, link in canais:
        payload = {
            "Nome": nome,
            "Link": link,
            "Capa": "https://imgur.com/vHEx37U.png",
            "Categoria": [int(ID_TABELA_CATEGORIAS)]
        }
        # Envia para a sua VPS
        requests.post(url, headers=headers, json=payload)
    print("[OK] Banco de dados na VPS atualizado!")

def minerar():
    # Fontes globais de links limpos
    fontes = [
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/br.m3u",
        "https://raw.githubusercontent.com/LITUATUI/IPTV/main/BR.m3u",
        "https://iptv-org.github.io/iptv/countries/br.m3u"
    ]
    
    lista_canais = []
    headers_br = {'User-Agent': 'Mozilla/5.0'}

    for url in fontes:
        try:
            r = requests.get(url, headers=headers_br, timeout=20)
            if r.status_code == 200:
                matches = re.findall(r'#EXTINF:.*?,(.*?)\n(https?://.*?\.m3u8.*)', r.text)
                for nome, link in matches:
                    n_up = nome.upper()
                    if any(p in n_up for p in ["SPORTV", "HBO", "PREMIERE", "ESPN", "DISCOVERY", "DISNEY", "NICK"]):
                        lista_canais.append((nome.strip(), link.strip()))
        except:
            continue

    final = list(set(lista_canais))
    
    if final:
        limpar_canais_antigos()
        subir_canais_novos(final)
    else:
        print("[!] Nenhum link funcional encontrado nos repositórios.")

if __name__ == "__main__":
    minerar()
