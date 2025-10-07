import os
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from biblioteca_playwright import iniciar_playwright

# Variáveis de ambiente seguras (Railway ou .env local)
SITE_USER = os.getenv("SITE_USER")
SITE_PASS = os.getenv("SITE_PASS")
SITE_URL_LOGIN = os.getenv("SITE_URL_LOGIN", "https://portal.mercurymarine.com.br/epdv/epdv001.asp")
SITE_URL_PRECO_BASE = os.getenv("SITE_URL_PRECO", "https://portal.mercurymarine.com.br/epdv/epdv002d2.asp")

async def executar_automacao(entrada):
    """Função genérica para teste de execução do Playwright."""
    navegador = iniciar_playwright()
    resultado = f"Automação executada com sucesso para: {entrada}"
    navegador.close()
    return resultado


async def pesqpreco_playwright(item: str):
    """
    Faz login no portal Mercury, pesquisa o item informado e retorna os dados da tabela.
    Login e URLs são carregados de variáveis de ambiente.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 🔒 Login
        print(f"[Playwright] Acessando {SITE_URL_LOGIN} com usuário {SITE_USER}")
        await page.goto(SITE_URL_LOGIN)
        await page.fill("input[name='sUsuar']", SITE_USER)
        await page.fill("input[name='sSenha']", SITE_PASS)
        await page.press("input[name='sSenha']", "Enter")
        await page.wait_for_load_state()

        # 🧭 Navegar para a página de pesquisa de preço
        url_pesquisa = (
            f"{SITE_URL_PRECO_BASE}"
            f"?s_nr_pedido_web=11111111111111111"
            f"&s_nr_tabpre=&s_fm_cod_com=null"
            f"&s_desc_item={item}"
        )
        print(f"[Playwright] Acessando página de pesquisa: {url_pesquisa}")
        await page.goto(url_pesquisa)
        await page.wait_for_load_state()

        # ⚙️ Verificar se há resultados
        no_records_element = await page.query_selector(".NoRecords")
        if no_records_element:
            print("[Playwright] Nenhum registro encontrado.")
            await browser.close()
            return []

        print("[Playwright] Item encontrado, extraindo dados...")

        # 🧩 Extrair HTML e processar com BeautifulSoup
        html_content = await page.content()
        soup = BeautifulSoup(html_content, "html.parser")

        form_preco_item_web = soup.find("form", id="preco_item_web")
        if not form_preco_item_web:
            print("[Playwright] Formulário 'preco_item_web' não encontrado.")
            await browser.close()
            return []

        first_table_in_form = form_preco_item_web.find("table")
        if not first_table_in_form:
            print("[Playwright] Primeira tabela dentro do formulário não encontrada.")
            await browser.close()
            return []

        tbody = first_table_in_form.find("tbody")
        if not tbody:
            print("[Playwright] Tbody da tabela principal não encontrado.")
            await browser.close()
            return []

        tr = tbody.find("tr")
        if not tr:
            print("[Playwright] Nenhum <tr> encontrado na tabela principal.")
            await browser.close()
            return []

        td = tr.find("td")
        if not td:
            print("[Playwright] Nenhum <td> encontrado na tabela principal.")
            await browser.close()
            return []

        tables_in_td = td.find_all("table")
        data_table = tables_in_td[1] if len(tables_in_td) > 1 else None

        if not data_table:
            print("[Playwright] Tabela de dados não encontrada.")
            await browser.close()
            return []

        linhas = data_table.find_all("tr", class_="Row")
        dados = []

        for linha in linhas:
            colunas = linha.find_all("td")
            if len(colunas) >= 8:
                dados_linha = {
                    "codigo": colunas[1].text.strip(),
                    "qtd": colunas[2].text.strip(),
                    "descricao": colunas[3].text.strip(),
                    "qtdaEst": colunas[4].text.strip(),
                    "valorVenda": colunas[5].text.strip(),
                    "valorTabela": colunas[6].text.strip(),
                    "valorCusto": colunas[7].text.strip(),
                }
                dados.append(dados_linha)

        await browser.close()
        print(f"[Playwright] {len(dados)} item(s) encontrados.")
        return dados
