import os
from playwright.sync_api import sync_playwright

def minerar():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) # No GitHub tem que ser True
        context = browser.new_context()
        page = context.new_page()
        
        # URL do site que você quer minerar (coloque a que você encontrou)
        url_alvo = "SUBSTITUA_PELA_URL_AQUI" 
        
        links = []
        # Captura links m3u8
        page.on("request", lambda request: links.append(request.url) if ".m3u8" in request.url else None)
        
        try:
            page.goto(url_alvo, wait_until="networkidle")
            page.wait_for_timeout(10000) # Espera 10 segundos para carregar o stream
        except:
            pass

        # Salva o que encontrou no arquivo lista.m3u
        if links:
            with open("lista.m3u", "w") as f:
                f.write("#EXTM3U\n")
                for i, link in enumerate(set(links)): # set() remove duplicados
                    f.write(f"#EXTINF:-1, Canal Minerado {i}\n{link}\n")
        
        browser.close()

if __name__ == "__main__":
    minerar()
