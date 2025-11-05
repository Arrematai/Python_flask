import os
import sys
import subprocess
import json
import time

from playwright.sync_api import sync_playwright

def run(self, headless):
    with sync_playwright() as p:
        # 🚀 Inicia navegador com perfil persistente
        context = p.chromium.launch_persistent_context(
            user_data_dir="/tmp/playwright-sodre",
            headless=False,  # ⚠️ Cloudflare precisa do modo visível
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--window-position=-32000,-32000",  # esconde janela
            ],
        )

        page = context.new_page()

        # 🕵️ Disfarça automação
        page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        window.chrome = { runtime: {} };
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        Object.defineProperty(navigator, 'languages', {get: () => ['pt-BR', 'pt']});
        Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
        """)

        print("🌐 Acessando Sodré Santoro...")
        page.goto("https://www.sodresantoro.com.br/veiculos", timeout=90000)
        page.wait_for_load_state("networkidle")

        # ⏳ Espera Cloudflare liberar cookie cf_clearance
        for _ in range(15):
            cookies = context.cookies()
            if any("cf_clearance" in c["name"] for c in cookies):
                print("✅ Cloudflare liberou acesso.")
                break
            time.sleep(1)
        else:
            print("⚠️ Cloudflare ainda não liberou. Encerrando.")
            context.close()
            return

        cookie_header = "; ".join(f"{c['name']}={c['value']}" for c in cookies)
        print(f"🍪 {len(cookies)} cookies carregados")

        # 📡 Faz a requisição real
        print("📡 Enviando requisição para /api/search-lots...")
        response = context.request.post(
            "https://www.sodresantoro.com.br/api/search-lots",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Origin": "https://www.sodresantoro.com.br",
                "Referer": "https://www.sodresantoro.com.br/veiculos",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/142.0.0.0 Safari/537.36",
                "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cookie": cookie_header,
            },
            data=json.dumps(self.payload),
        )

        print("🔎 Status:", response.status)
        if response.status == 200:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print("❌ Erro:", response.text())

        context.close()
        print(response)
        
        return response