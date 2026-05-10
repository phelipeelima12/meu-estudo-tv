import os
import re
import base64
from playwright.sync_api import sync_playwright

def minerar():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # --- CONFIGURAÇÃO DO SEU PROXY WORKER ---
        meu_worker = "https://round-morning-1174.paginainsta32.workers.dev"
        site_de_tv = "https://canaistops.club/aovivo/sportv-ao-vivo-live-online-gratis/"
        
        # Aqui o robô pede para o Worker buscar o site pra ele
        url_alvo = f"{meu_worker}/?url={site_de_tv}"
        # ----------------------------------------

        links = []
        print(f"[*] Minerando via Proxy Worker: {url_alvo}")
        
        try:
            # O Worker entrega o HTML e o Playwright analisa
            page.goto(url_alvo, wait_until="load", timeout=60000)
            page.wait_for_timeout(15000)

            # Pega o conteúdo que o Worker trouxe
            content = page.content()
            
            # BUSCA 1: Regex direta por links .m3u8
            regex_m3u8 = r'(https?://[^\s"\']+\.m3u8[^\s"\']*)'
            links.extend(re.findall(regex_m3u8, content))

            # BUSCA 2: Decodificação de Base64 (comum em canais fechados)
            b64_pattern = r'["\']([A-Za-z0-9+/]{40,})["\']'
            for match in re.findall(b64_pattern, content):
                try:
                    decoded = base64.b64decode(match).decode('utf-8')
                    if ".m3u8" in decoded:
                        links.append(decoded)
                except:
                    continue

        except Exception as e:
            print(f"[!] Erro na mineração: {e}")

        # Limpeza: remove duplicados e links de anúncios
        valid_links = sorted(set([l for l in links if "http" in l and "ads" not in l.lower()]))
        
        with open("lista.m3u", "w") as f:
            f.write("#EXTM3U\n")
            if not valid_links:
                f.write("# INFO: O Worker trouxe o site, mas o link m3u8 nao foi encontrado no codigo.\n")
            else:
                print(f"[OK] {len(valid_links)} links encontrados!")
                for i, link in enumerate(valid_links):
                    f.write(f"#EXTINF:-1, Canal Minerado {i+1}\n{link}\n")
        
        browser.close()

if __name__ == "__main__":
    minerar()
