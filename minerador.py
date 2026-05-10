import requests
import re

def minerar_repositorios():
    # Lista de fontes (GitHub, Gists e Repositórios conhecidos)
    # Estes links são de texto puro (RAW), o que facilita a mineração
    fontes = [
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/br.m3u", # Canais BR
        "https://raw.githubusercontent.com/LITUATUI/IPTV/main/BR.m3u",           # Outro Repo BR
        "https://iptv-org.github.io/iptv/countries/br.m3u"                      # API IPTV-Org
    ]
    
    print("[*] Iniciando a varredura de fontes globais...")
    links_finais = []

    for url in fontes:
        try:
            print(f"[*] Escaneando: {url}")
            # Simulando um navegador para não ser bloqueado
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # Regex para pegar o nome do canal e o link m3u8
                # O padrão procura por #EXTINF seguido do nome e o link na linha de baixo
                padrao = re.findall(r'#EXTINF:.*?,(.*?)\n(https?://.*?\.m3u8.*)', response.text)
                
                for nome, link in padrao:
                    # Filtra apenas canais que parecem ser "fechados" (Premium)
                    # Você pode adicionar mais palavras aqui conforme sua necessidade
                    palavras_premium = ["HBO", "SPORTV", "PREMIERE", "DISCOVERY", "NICK", "ESPN", "DISNEY", "AXN"]
                    
                    if any(p in nome.upper() for p in palavras_premium):
                        links_finais.append((nome.strip(), link.strip()))
        except Exception as e:
            print(f"[!] Erro ao acessar {url}: {e}")
            continue

    # Gerando o arquivo lista.m3u final
    with open("lista.m3u", "w") as f:
        f.write("#EXTM3U\n")
        if not links_finais:
            f.write("# INFO: Nenhuma fonte premium encontrada nos repositorios hoje.\n")
        else:
            print(f"[OK] {len(links_finais)} canais fechados encontrados!")
            for nome, link in set(links_finais): # set() para evitar duplicados
                f.write(f"#EXTINF:-1, {nome}\n{link}\n")

if __name__ == "__main__":
    minerar_repositorios()
