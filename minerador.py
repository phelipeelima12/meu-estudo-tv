import os
from playwright.sync_api import sync_playwright

def minerar():
    with sync_playwright() as p:
        # 1. Configuração do navegador (Simulando um PC comum para evitar bloqueios)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 720}
        )
        page = context.new_page()
        
        # 2. URL ALVO (O canal que você escolheu)
        url_alvo = "https://canaistops.club/aovivo/sportv-ao-vivo-live-online-gratis/" 
        
        links = []

        # 3. Capturador de tráfego de rede (O "Pescador")
        def handle_request(request):
            url = request.url.lower()
            # Filtra por extensões e padrões comuns de streaming de canais fechados
            if any(ext in url for ext in [".m3u8", "playlist.m3u8", "chunklist", "stream.m3u8"]):
                if request.url not in links:
                    # Ignora links de anúncios conhecidos para limpar a lista
                    if "ads" not in url and "telemetry" not in url:
                        links.append(request.url)

        page.on("request", handle_request)
        
        print(f"[*] Iniciando mineração no alvo: {url_alvo}")
        
        try:
            # 4. Acessa a página
            page.goto(url_alvo, wait_until="domcontentloaded", timeout=60000)
            print("[*] Página carregada. Aguardando anúncios iniciais...")
            page.wait_for_timeout(10000) # 10 segundos para os banners aparecerem
            
            # 5. Lógica de "Limpeza" e Play
            # Clica em 3 pontos diferentes para garantir que fechou popups e deu play
            pontos_de_clique = [(640, 360), (640, 400), (600, 300)]
            for x, y in pontos_de_clique:
                print(f"[*] Tentando clique em {x}, {y}...")
                page.mouse.click(x, y)
                page.wait_for_timeout(3000) # Espera 3s entre cliques para o site reagir

            # 6. Tempo de espera final para o stream começar a rodar
            print("[*] Aguardando captura final do stream...")
            page.wait_for_timeout(30000) 
            
        except Exception as e:
            print(f"[!] Erro durante o processo: {e}")

        # 7. Salva os resultados no arquivo que o GitHub Actions vai ler
        if not links:
            print("[!] Nenhum link de canal foi encontrado. Tente outra URL ou aumente o tempo.")
            with open("lista.m3u", "w") as f:
                f.write("#EXTM3U\n# INFO: Nenhum canal encontrado. Verifique se o site mudou o player.\n")
        else:
            print(f"[OK] Sucesso! Encontramos {len(links)} possíveis links de stream.")
            with open("lista.m3u", "w") as f:
                f.write("#EXTM3U\n")
                # Salva os links encontrados
                for i, link in enumerate(sorted(set(links))):
                    f.write(f"#EXTINF:-1, Canal Minerado {i+1}\n{link}\n")
        
        browser.close()

if __name__ == "__main__":
    minerar()
