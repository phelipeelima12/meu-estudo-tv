import os
import re
import base64
from playwright.sync_api import sync_playwright

def minerar():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # --- CONFIGURAÇÃO DO SEU PROXY ---
        meu_worker = "https://round-morning-1174.paginainsta32.workers.dev/"
        site_alvo = "https://canaistops.club/aovivo/sportv-ao-vivo-live-online-gratis/"
        
        # A URL final que o robô vai acessar
        url_com_proxy = f"{meu_worker}/?url={site_alvo}"
        # ---------------------------------

        links = []
        print(f"[*] Minerando via Proxy: {url_com_proxy}")
        
        try:
            page.goto(url_com_proxy, wait_until="load", timeout=60000)
            # O resto do código (Regex e Base64) continua igual...
            page.wait_for_timeout(15000)

            # 2. ATAQUE DE SCRAPING: Busca links escondidos no código HTML
            content = page.content()
            
            # Busca padrões de links m3u8 em texto ou escondidos em aspas
            regex_m3u8 = r'(https?://[^\s"\']+\.m3u8[^\s"\']*)'
            achados_no_html = re.findall(regex_m3u8, content)
            links.extend(achados_no_html)

            # 3. ATAQUE DE BASE64: Muitos sites escondem o link em Base64
            # Busca strings longas que podem ser links codificados
            b64_pattern = r'["\']([A-Za-z0-9+/={4,})["\']'
            for match in re.findall(b64_pattern, content):
                try:
                    decoded = base64.b64decode(match).decode('utf-8')
                    if ".m3u8" in decoded:
                        links.append(decoded)
                except:
                    continue

        except Exception as e:
            print(f"[!] Erro: {e}")

        # Salva os resultados
        valid_links = sorted(set([l for l in links if "http" in l and "ads" not in l.lower()]))
        
        with open("lista.m3u", "w") as f:
            f.write("#EXTM3U\n")
            if not valid_links:
                f.write("# INFO: O site bloqueou o robô. Tente usar o Cloudflare Worker como Proxy.\n")
            else:
                for i, link in enumerate(valid_links):
                    f.write(f"#EXTINF:-1, Canal Minerado {i+1}\n{link}\n")
        
        browser.close()

if __name__ == "__main__":
    minerar()
