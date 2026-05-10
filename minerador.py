import os
import re
import base64
from playwright.sync_api import sync_playwright

def minerar():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # --- SEU WORKER (JÁ ESTÁ FUNCIONANDO!) ---
        meu_worker = "https://round-morning-1174.paginainsta32.workers.dev"
        # Tente mudar este site abaixo para outro agregador se o anterior continuar dando DRM
        site_de_tv = "https://canaistops.club/aovivo/sportv-ao-vivo-live-online-gratis/"
        url_alvo = f"{meu_worker}/?url={site_de_tv}"
        # ----------------------------------------

        links_encontrados = []
        
        # Intercepta links m3u8 que passam "voando" pela rede
        page.on("request", lambda r: links_encontrados.append(r.url) if ".m3u8" in r.url.lower() else None)

        print(f"[*] Iniciando Scanner Profissional via Proxy...")
        
        try:
            page.goto(url_alvo, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(20000)

            # Pega o código-fonte bruto
            html = page.content()
            
            # BUSCA 1: Links em texto puro (Regex)
            links_encontrados.extend(re.findall(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', html))

            # BUSCA 2: Links em Base64
            b64_matches = re.findall(r'["\']([A-Za-z0-9+/]{40,})["\']', html)
            for b in b64_matches:
                try:
                    dec = base64.b64decode(b).decode('utf-8')
                    if ".m3u8" in dec: links_encontrados.append(dec)
                except: continue

        except Exception as e:
            print(f"Erro: {e}")

        # --- FILTRO DE QUALIDADE ---
        # Remove lixo, anúncios e duplicados
        limpos = []
        for l in set(links_encontrados):
            if "http" in l and ".m3u8" in l.lower():
                if not any(x in l.lower() for x in ["ads", "telemetry", "google", "fbcdn"]):
                    limpos.append(l)

        # GRAVAÇÃO FINAL
        with open("lista.m3u", "w") as f:
            f.write("#EXTM3U\n")
            if not limpos:
                f.write("# INFO: Este site especifico usa DRM forte. Tente outro agregador no minerador.py\n")
            else:
                for i, link in enumerate(sorted(limpos)):
                    f.write(f"#EXTINF:-1, Canal Minerado {i+1}\n{link}\n")
        
        browser.close()

if __name__ == "__main__":
    minerar()
