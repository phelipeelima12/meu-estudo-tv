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
        
        # --- SUA ESTRUTURA JÁ FUNCIONAL ---
        meu_worker = "https://round-morning-1174.paginainsta32.workers.dev"
        site_de_tv = "https://canaistops.club/aovivo/sportv-ao-vivo-live-online-gratis/"
        url_alvo = f"{meu_worker}/?url={site_de_tv}"
        # ----------------------------------

        links_brutos = []
        
        # Captura links que passam pela rede enquanto o Worker carrega o HTML
        page.on("request", lambda r: links_brutos.append(r.url) if ".m3u8" in r.url.lower() else None)

        print(f"[*] Escaneando: {url_alvo}")
        
        try:
            page.goto(url_alvo, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(10000)

            # Pega o HTML que o Worker trouxe
            html_content = page.content()
            
            # 1. BUSCA POR REGEX (Links diretos no código)
            # Procura links m3u8 em aspas simples, duplas ou soltos
            padrao_direto = r'["\'](https?://[^\s"\']+\.m3u8[^\s"\']*)["\']'
            links_brutos.extend(re.findall(padrao_direto, html_content))

            # 2. BUSCA POR STRINGS EMBUTIDAS (Onde o link fica escondido)
            # Procura por qualquer coisa que pareça um link de stream
            padrao_generico = r'(https?://[^\s"\']+/playlist\.m3u8[^\s"\']*)'
            links_brutos.extend(re.findall(padrao_generico, html_content))

            # 3. DECODIFICADOR DE SEGURANÇA (Base64)
            # Procura blocos longos de texto que podem ser links codificados
            blocos_suspeitos = re.findall(r'["\']([A-Za-z0-9+/]{50,})["\']', html_content)
            for bloco in blocos_suspeitos:
                try:
                    decodificado = base64.b64decode(bloco).decode('utf-8')
                    if "http" in decodificado and ".m3u8" in decodificado:
                        links_brutos.append(decodificado)
                except:
                    continue

        except Exception as e:
            print(f"[!] Erro: {e}")

        # --- LIMPEZA E VALIDAÇÃO ---
        links_finais = []
        for l in set(links_brutos):
            # Filtra links de propaganda e garante que seja uma URL válida
            l_lower = l.lower()
            if "http" in l_lower and ".m3u8" in l_lower:
                if not any(x in l_lower for x in ["ads", "popunder", "telemetry", "google", "facebook"]):
                    links_finais.append(l)

        # Grava o resultado para o seu App Roku/Android
        with open("lista.m3u", "w") as f:
            f.write("#EXTM3U\n")
            if not links_finais:
                f.write("# INFO: O sinal foi capturado mas o link real esta protegido por DRM ou Token Dinamico.\n")
                print("[!] Nada encontrado.")
            else:
                print(f"[OK] Encontramos {len(links_finais)} links!")
                for i, link in enumerate(sorted(links_finais)):
                    f.write(f"#EXTINF:-1, Canal Minerado {i+1}\n{link}\n")
        
        browser.close()

if __name__ == "__main__":
    minerar()
