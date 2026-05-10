import requests
import re

def minerar_fontes_reais():
    # Estas URLs são repositórios que atualizam canais premium constantemente
    fontes = [
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/br.m3u",
        "https://raw.githubusercontent.com/LITUATUI/IPTV/main/BR.m3u",
        "https://iptv-org.github.io/iptv/countries/br.m3u"
    ]
    
    print("[*] Iniciando busca em repositórios de alta disponibilidade...")
    canais_encontrados = []
    
    for url in fontes:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                # Extrai o nome do canal e o link m3u8
                matches = re.findall(r'#EXTINF:.*?,(.*?)\n(https?://.*?\.m3u8.*)', r.text)
                for nome, link in matches:
                    nome_up = nome.upper()
                    # Filtra apenas o que você quer (Canais Fechados)
                    if any(p in nome_up for p in ["SPORTV", "HBO", "PREMIERE", "ESPN", "DISCOVERY", "DISNEY", "NICK"]):
                        canais_encontrados.append((nome.strip(), link.strip()))
        except:
            continue

    # Remove duplicados e salva
    canais_unicos = sorted(set(canais_encontrados))
    
    with open("lista.m3u", "w") as f:
        f.write("#EXTM3U\n")
        if not canais_unicos:
            f.write("# INFO: Nenhuma fonte premium ativa encontrada agora. Rode novamente em 1 hora.\n")
        else:
            print(f"[OK] {len(canais_unicos)} canais fechados minerados com sucesso!")
            for nome, link in canais_unicos:
                f.write(f"#EXTINF:-1, {nome}\n{link}\n")

if __name__ == "__main__":
    minerar_fontes_reais()
