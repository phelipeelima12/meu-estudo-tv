import os
from playwright.sync_api import sync_playwright

def minerar():
    with sync_playwright() as p:
        # Usando um User-Agent de Smart TV para evitar bloqueios
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (SmartHub; SMART-TV; Samsung; LGWebOS) AppleWebKit/537.36 (KHTML, like Gecko) TV Safari/537.36"
        )
        page = context.new_page()
        
        # COLOQUE A URL DO SITE AQUI
        url_alvo = "SUBSTITUA_PELA_URL_AQUI" 
        
        links = []
        # Captura links m3u8
        page.on("request", lambda request: links.append(request.url) if ".m3u8" in request.url else None)
        
        print(f"Iniciando captura em: {url_alvo}")
        
        try:
            # Espera até a rede ficar ociosa
            page.goto(url_alvo, wait_until="networkidle", timeout=60000)
            # Espera o player carregar de fato
            page.wait_for_timeout(20000) 
        except Exception as e:
            print(f"Erro no acesso: {e}")

        # Garante que o arquivo seja criado para não dar erro no GitHub Actions
        if not links:
            print("Nenhum link m3u8 encontrado desta vez.")
            with open("lista.m3u", "w") as f:
                f.write("#EXTM3U\n# INFO: Nenhum canal encontrado na ultima varredura.")
        else:
            print(f"Sucesso! {len(links)} links encontrados.")
            with open("lista.m3u", "w") as f:
                f.write("#EXTM3U\n")
                for i, link in enumerate(set(links)):
                    f.write(f"#EXTINF:-1, Canal Minerado {i}\n{link}\n")
        
        browser.close()

if __name__ == "__main__":
    minerar()
