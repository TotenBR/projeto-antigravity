# 📊 PROJETO FIIs & FIAGROS - Automação e Consolidação
*(Cor recomendada no Google Keep: **Ciano (Teal)** ou **Azul**)*

---

### 📌 1. OBJETIVO DO PROJETO
Buscar na internet de forma autônoma relatórios gerenciais/mensais (PDFs) de uma lista de fundos imobiliários (FIIs/Fiagros), extrair trechos importantes (focando em riscos, vacância e alocação) e consolidar os dados em um relatório executivo PDF altamente profissional.

---

### ⚙️ 2. MCPs NECESSÁRIOS (INFRAESTRUTURA)
Ative estes servidores MCP nas configurações do seu cliente Antigravity:
*   [ ] **Google Search MCP**: Para localizar as páginas de RI de cada fundo via busca web em tempo real.
*   [ ] **Fetch MCP**: Para acessar URLs de Relações com Investidores e inicializar o download de arquivos PDF.
*   [ ] **Filesystem MCP**: Para ler a lista inicial de ativos (`LISTA DE FIIS.txt`) e salvar o relatório PDF final no HD do computador.

---

### 📦 3. DEPENDÊNCIAS & BIBLIOTECAS (PYTHON)
Instale as seguintes dependências no ambiente virtual (`venv`):
```bash
pip install beautifulsoup4 pypdf reportlab
```
*   `beautifulsoup4` (bs4): Usada para fazer o parsing dos resultados das páginas de busca e extrair links dos PDFs.
*   `pypdf`: Usada para abrir os relatórios baixados, fazer buscas por termos-chave e extrair o texto de páginas relevantes.
*   `reportlab` / `google-chrome` (Headless): Utilizados para desenhar e renderizar o PDF final (o script `gerar_pdf.py` utiliza o Google Chrome Headless para imprimir um arquivo HTML/CSS estruturado para PDF, contornando limitações de design do ReportLab).

---

### 🤖 4. HABILIDADES DO AGENTE (AGENT SKILLS)
Criadas em `/.agent/skills/` para guiar a IA na execução padrão:

#### 📂 Skill 1: `/mapear-ri`
*   **Finalidade:** Ler a lista de ativos, pesquisar no buscador por relatórios em PDF, efetuar o download de até 2 relatórios recentes por FII e salvá-los temporariamente em `/.temp/`.
*   **Caminho:** `/.agent/skills/mapear-ri/agent/skill.md`

#### 📂 Skill 2: `/sintetizar-relatorios`
*   **Finalidade:** Analisar os PDFs na pasta temporária, extrair tese de investimentos, riscos (vacância, alavancagem, inadimplência) e recomendações. Compilar tudo em um arquivo de saída consolidado.
*   **Caminho:** `/.agent/skills/sintetizar-relatorios/agent/skill.md`

---

### 📂 5. SCRIPTS CONSTRUÍDOS
#### 📄 `mapear_ri.py`
Executa busca concorrente (via `ThreadPoolExecutor`) no Yahoo Search com strings do tipo `"{ticker} relatorio gerencial pdf"`, baixa os arquivos validando os bytes mágicos `%PDF` e abre a pasta de downloads no sistema via `xdg-open` ou subprocesso.

#### 📄 `extract_data.py`
Lê os PDFs em `/.temp/`, extrai as primeiras 3 páginas e faz escaneamento textual das demais páginas procurando por palavras-chave (`vacância`, `inadimplência`, `alavancagem`, `risco`, `dividendo`). Limita a extração a 15k caracteres por relatório para não estourar a janela de contexto e salva tudo em `extracted_text.json`.

#### 📄 `gerar_pdf.py`
Consolida as análises estruturadas de cada fundo imobiliário em um template HTML com CSS moderno (fontes personalizadas, cores harmoniosas, badges de nível de alerta de 1 a 10) e executa o comando `google-chrome --headless --print-to-pdf` para gerar o relatório consolidado final com estética premium.

---

### 💬 6. PROMPT MESTRE DE CONSTRUÇÃO (Copiar para iniciar novo projeto)
> "Quero criar uma automação em Python para análise de Fundos Imobiliários. 
> 1. Leia um arquivo `LISTA DE FIIS.txt` contendo tickers (um por linha).
> 2. Faça buscas na web para encontrar e baixar os 2 relatórios gerenciais mais recentes de cada fundo em formato PDF para uma pasta `.temp/`.
> 3. Crie um script de extração usando `pypdf` para minerar dados focando em 'vacância', 'inadimplência', 'alavancagem', 'comentários do gestor' e 'dividendos'. Limite o contexto extraído por arquivo.
> 4. Crie um script que compile estes dados em uma página HTML visualmente atraente (com visual moderno, badges de cores para riscos/alertas) e converta em PDF executivo consolidado usando o Google Chrome em modo headless."

---

### 🚀 7. RECOMENDAÇÕES E NOVOS AGENTES
*   [ ] **Agente Macro (MacroAI):** Adicionar um agente secundário especialista em macroeconomia para ler notícias de juros (Selic, IPCA, boletim Focus) e cruzar com os dados dos fundos para prever dividendos.
*   [ ] **Bibliotecas Adicionais:** Utilizar `pdfplumber` se precisar extrair tabelas financeiras complexas (como DRE) com mais precisão do que a leitura crua do `pypdf`.
*   [ ] **Alertas Automatizados:** Integrar um script que envie o PDF consolidado diretamente para um canal do Telegram ou e-mail toda vez que houver mudança na lista.
