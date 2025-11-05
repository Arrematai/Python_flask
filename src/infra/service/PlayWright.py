import json
import time
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError


def build_payload(query = "",size=20,playload = {}):
    p = playload.copy()
    # Deep copy safer for nested structures
    p = json.loads(json.dumps(playload))
    p["size"] = size
    # p["query"]["bool"]["must"][0]["match_phrase_prefix"]["search_terms"] = query
    return p


def run_search(query: str, size: int = 20, headless: bool = True, retries: int = 0, playload = {}):
    base_list_url = f"https://www.sodresantoro.com.br/atendimento"
    api_url = "https://www.sodresantoro.com.br/api/search-lots"

    payload = build_payload(query="",size=size, playload=playload)

    # Ajuste: se quiser enviar query string no corpo, pode adaptar aqui.
    # payload["query_string"] = query  # caso necessário

    attempt = 0
    last_error = None

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless)
        context = browser.new_context()  # cria contexto limpo (cookies isolados)
        page = context.new_page()

        try:
            # Acesse a página de listagem para que os cookies/JS carreguem
            # print(f"[+] Navigating to {base_list_url} to initialize session...")
            page.goto(base_list_url, timeout=30000)
            # Espera um pouco para o JS estabelecer cookies/tokens; ajuste se necessário
            page.wait_for_timeout(1000)

            # opcional: aceitar popups/consent banners (exemplo genérico)
            # tentar clicar em botões comuns (não garantido em todo site)
            try:
                page.locator("button:has-text('Aceitar'), button:has-text('Aceito'), button:has-text('OK')").first.click(timeout=1000)
                # print("[*] Possible cookie banner closed")
            except Exception:
                pass

            while attempt <= retries:
                attempt += 1
                print(f"[+] Attempt {attempt} to fetch API inside page context...")

                try:
                    # Executa fetch dentro do navegador (herda cookies e contexto)
                    result = page.evaluate(
                        """async ({api_url, payload}) => {
                            try {
                                const res = await fetch(api_url, {
                                    method: "POST",
                                    headers: {
                                        "accept": "application/json, text/plain, */*",
                                        "content-type": "application/json",
                                        // note: não setamos cookies aqui — o browser já envia
                                    },
                                    body: JSON.stringify(payload),
                                    credentials: 'include',
                                });
                                const text = await res.text();
                                let json = null;
                                try {
                                    json = JSON.parse(text);
                                } catch(e) {
                                    // pode não ser JSON
                                    return { ok: false, status: res.status, text };
                                }
                                return { ok: true, status: res.status, json };
                            } catch (err) {
                                return { ok: false, error: String(err) };
                            }
                        }""",
                        {"api_url": api_url, "payload": payload},
                    )

                    if not isinstance(result, dict):
                        last_error = f"Unexpected result type: {type(result)}"
                        print("[-]", last_error)
                        time.sleep(2)
                        continue

                    if result.get("ok"):
                        status = result.get("status")
                        data = result.get("json")
                        # print(f"[+] API returned status {status}.")
                        if data:
                            return data
                        # resumir e sair
                        total_hits = None
                        try:
                            # estrutura pode variar, tentamos encontrar total hits
                            if isinstance(data, dict):
                                if "hits" in data and isinstance(data["hits"], dict):
                                    total_hits = data["hits"].get("total")
                                elif "total" in data:
                                    total_hits = data.get("total")
                        except Exception:
                            total_hits = None
                        print(f"[+] Total hits (possible): {total_hits}")
                        browser.close()
                        return data
                    else:
                        # resultado de erro (resposta não JSON ou status != 200)
                        last_error = result
                        print("[-] Fetch returned not ok:", result)
                        # aguardar backoff e tentar novamente
                        time.sleep(2 ** attempt)
                except PWTimeoutError as e:
                    last_error = e
                    print("[-] Playwright timeout:", str(e))
                    time.sleep(2 ** attempt)
                except Exception as e:
                    last_error = e
                    print("[-] Unexpected error:", str(e))
                    time.sleep(2 ** attempt)

            browser.close()
            raise RuntimeError(f"Failed to fetch API after {retries+1} attempts. Last error: {last_error}")
        finally:
            context.close()