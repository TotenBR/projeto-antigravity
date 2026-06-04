import os
import re
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

WORKSPACE = "/home/toten/projeto-antigravity"
DATA_JS = os.path.join(WORKSPACE, "data.js")
EXTRACTED_JSON = os.path.join(WORKSPACE, ".temp", "extracted_text.json")

def load_current_data(filepath):
    """Lê o arquivo data.js e extrai o dicionário de FIIs atual."""
    if not os.path.exists(filepath):
        print(f"Arquivo {filepath} não encontrado.")
        return {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontra o bloco entre as chaves { ... }
    match = re.search(r'const fiisData\s*=\s*(\{.*\});?', content, re.DOTALL)
    if not match:
        # Tenta pegar apenas o bloco JSON caso não tenha const fiisData
        match = re.search(r'(\{.*\})', content, re.DOTALL)
        
    if match:
        try:
            return json.loads(match.group(1))
        except Exception as e:
            print(f"Erro ao converter data.js para JSON: {e}")
    return {}

def save_data(filepath, data):
    """Regrava o arquivo data.js estruturado como constante JavaScript."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("const fiisData = ")
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print(f"Base de dados atualizada com sucesso em {filepath}")

def analyze_fii(client, ticker, name, report_text):
    """Usa a API do Gemini para analisar os textos dos PDFs e gerar as teses em formato JSON."""
    print(f"[{ticker}] Enviando dados dos relatórios gerenciais para análise do Gemini...")
    
    prompt = f"""
Você é um especialista certificado em análise de fundos imobiliários (FIIs, Fiagros e FI-Infras) na B3.
Seu objetivo é analisar os trechos extraídos do relatório mensal recente do fundo {ticker} ({name}) e retornar um JSON contendo uma análise de qualidade CNPI.

Textos extraídos do Relatório Gerencial de {ticker}:
---
{report_text}
---

Gere uma resposta em JSON estrito contendo os seguintes campos:
{{
  "recomendacao": "Comprar" ou "Manter" ou "Vender",
  "alerta": <inteiro de 1 a 10 representando o nível de risco e cautela>,
  "explicacoes": "Explicação técnica e resumida da tese de investimento deste ativo, destacando portfólio, gestão e contratos. Máximo 4 frases.",
  "pontos_criticos": "Riscos específicos identificados no relatório, como alavancagem, vacância, inadimplência, ou vencimento de contratos importantes. Máximo 3 frases.",
  "boas_noticias": "Eventos favoráveis recentes, como novas locações, vendas favoráveis, reajustes inflacionários ou queda na vacância. Máximo 2 frases.",
  "tendencia_preco": "subir" ou "cair" ou "manter",
  "tendencia_dividendos": "aumentar" ou "cair" ou "manter"
}}

Importante:
1. Certifique-se de que a resposta seja APENAS o JSON, sem blocos explicativos adicionais.
2. Seja realista: se o relatório aponta problemas graves de vacância ou calote, a recomendação deve mudar para "Manter" ou "Vender" e a nota de risco ("alerta") deve subir.
3. Se a informação sobre tendências ou risco for implícita, faça uma inferência fundamentada com base nos dados do relatório.
"""

    try:
        # Utiliza o modelo gemini-2.5-flash por ser rápido, inteligente e econômico
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            ),
        )
        
        # Faz o parse da resposta
        res_json = json.loads(response.text)
        return res_json
    except Exception as e:
        print(f"[{ticker}] Erro na chamada à API do Gemini: {e}")
        return None

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Erro: A variável de ambiente GEMINI_API_KEY não está configurada no seu arquivo .env!")
        return

    # Inicializa o cliente do SDK google-genai
    client = genai.Client()

    # Carrega dados atuais
    fiis_data = load_current_data(DATA_JS)
    if not fiis_data:
        print("Não foi possível carregar os FIIs atuais do data.js. Abortando.")
        return

    # Carrega relatórios extraídos
    if not os.path.exists(EXTRACTED_JSON):
        print(f"Arquivo de textos extraídos {EXTRACTED_JSON} não encontrado. Execute o extract_data.py primeiro.")
        return

    with open(EXTRACTED_JSON, 'r', encoding='utf-8') as f:
        extracted_data = json.load(f)

    updated_count = 0
    for ticker, reports in extracted_data.items():
        if ticker not in fiis_data:
            print(f"Aviso: Ticker {ticker} encontrado no relatório mas não cadastrado no data.js. Ignorando ou criando novo.")
            continue
        
        # Junta o texto de todas as páginas extraídas deste ativo
        report_text = ""
        for rep in reports:
            report_text += f"\n--- Arquivo: {rep['filename']} ---\n{rep['content']}\n"
        
        # Executa análise via Gemini
        analysis = analyze_fii(client, ticker, fiis_data[ticker].get("nome", ""), report_text)
        
        if analysis:
            # Atualiza os campos relevantes mantendo o histórico de dividendos e outros intocados
            fiis_data[ticker]["recomendacao"] = analysis.get("recomendacao", fiis_data[ticker].get("recomendacao", "Manter"))
            fiis_data[ticker]["alerta"] = analysis.get("alerta", fiis_data[ticker].get("alerta", 5))
            fiis_data[ticker]["explicacoes"] = analysis.get("explicacoes", fiis_data[ticker].get("explicacoes", ""))
            fiis_data[ticker]["pontos_criticos"] = analysis.get("pontos_criticos", fiis_data[ticker].get("pontos_criticos", ""))
            fiis_data[ticker]["boas_noticias"] = analysis.get("boas_noticias", fiis_data[ticker].get("boas_noticias", ""))
            fiis_data[ticker]["tendencia_preco"] = analysis.get("tendencia_preco", fiis_data[ticker].get("tendencia_preco", "manter"))
            fiis_data[ticker]["tendencia_dividendos"] = analysis.get("tendencia_dividendos", fiis_data[ticker].get("tendencia_dividendos", "manter"))
            
            print(f"[{ticker}] Sucesso: Recom: {fiis_data[ticker]['recomendacao']} | Alerta: {fiis_data[ticker]['alerta']}")
            updated_count += 1
            
    if updated_count > 0:
        save_data(DATA_JS, fiis_data)
        print(f"\nPipeline finalizado. {updated_count} ativos analisados e atualizados pela IA!")
    else:
        print("\nNenhuma análise nova pôde ser aplicada. Verifique se os PDFs estão corretos.")

if __name__ == '__main__':
    main()
