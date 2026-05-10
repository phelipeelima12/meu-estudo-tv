import requests
import re

# --- CONFIGURAÇÕES DA SUA VPS ---
BASE_URL = "http://213.199.56.115"
TOKEN_BASEROW = "KFB2YupQfqQZj6kFDwO6NKaje07vd6DP"
ID_TABELA_CONTEUDOS = "1186"
ID_CATEGORIA_CANAIS = 22 # Categoria 'Canais'

def enviar_vps(nome, link):
    url = f"{BASE_URL}/api/database/rows/table/{ID_TABELA_CONTEUDOS}/?user_field_names=true"
    headers = {
        "Authorization": f"Token {TOKEN_BASEROW}",
        "Content-Type": "application/json"
    }
    
    # Payload simplificado para teste
    payload = {
        "Nome": nome,
        "Link": link,
        "Capa": "https://imgur.com/vHEx37U.png",
        "Categoria": [ID_CATEGORIA_CANAIS]
    }
    
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        if r.status_code not in [200, 201]:
            print(f"[!] Erro da VPS ao adicionar {nome}: {r.status_code} - {r.text}")
        return r.status_code
    except Exception as e:
        print(f"[!] Falha total de conexão com a VPS: {e}")
        return 500

def minerar():
    # Fontes alternativas e diretas para não falhar a busca
    fontes = [
        "https://iptv-org.github.io/iptv/countries/br.m3u",
        "https://raw.githubusercontent.com/LITUATUI/IPTV/main/BR.m3u"
    ]
    
    print(f"[*] Iniciando teste de carga na VPS: {BASE_URL}")
    canais_encontrados = []
    
    for url in fontes:
        try:
            print(f"[*] Lendo: {url}")
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                # Regex que aceita quase qualquer formato de nome
                matches = re.findall(r'#EXTINF:.*?,(.*?)\n(https?://.*?\.m3u8.*)', r.text)
                for nome, link in matches:
                    # Se encontrar qualquer coisa que pareça canal, adiciona para teste
                    if len(nome) > 2:
                        canais_encontrados.append((nome.strip(), link.strip()))
        except:
            continue

    # Remove duplicados
    lista = list(set(canais_encontrados))
    print(f"[*] Canais encontrados no total: {len(lista)}")

    if lista:
        sucesso = 0
        # Tenta subir os primeiros 10 para ver se a VPS aceita
        for nome, link in lista[:10]:
            status = enviar_vps(nome, link)
            if status in [200, 201]:
                sucesso += 1
                print(f"[OK] Adicionado: {nome}")
        
        print(f"\n[FIM] Sucesso em {sucesso} de 10 tentativas.")
    else:
        print("[!] O robô não encontrou NENHUM link nas fontes. Verifique se as URLs das fontes abrem no seu navegador.")

if __name__ == "__main__":
    minerar()
