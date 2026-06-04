# ⚖️ PROJETO PESQUISA PROCESSUAL - TJMG & DJEN
*(Cor recomendada no Google Keep: **Amarelo (Yellow)** ou **Laranja (Orange)**)*

---

### 📌 1. OBJETIVO DO PROJETO
Pesquisar andamentos, decisões e publicações de um processo judicial específico em portais de tribunais (como o TJMG) e diários oficiais (DJEN/DJE), tratar inconsistências de numeração única CNJ e gerar um Relatório Jurídico Executivo profissional de até 5 páginas.

---

### ⚙️ 2. MCPs E INFRAESTRUTURA NECESSÁRIOS
*   [ ] **Puppeteer MCP / Playwright MCP**: Essencial para navegar em portais de tribunais dinâmicos (renderização de JS, preenchimento de formulários, cliques e extração de dados).
*   [ ] **Browser / Screenshot MCP**: Para visualização em tempo real das páginas do tribunal para resolução de captchas manuais pelo usuário ou validação de layouts de busca.
*   [ ] **Filesystem MCP**: Para manipulação de arquivos locais e armazenamento dos relatórios em PDF.

---

### 🤖 3. ARQUITETURA DE AGENTES JURÍDICOS (SUGESTÃO)
*   **Agente Paralegal de Consulta (JurisBot):** Configurado especificamente para entender formulários de busca do e-Saj, PJe ou PROJUDI.
*   **Agente de Clipping e Pesquisa Pública:** Especializado em vasculhar diários eletrônicos (DJE/DJEN) e extrair os parágrafos exatos de menção ao nome/processo.
*   **Agente Consultor Jurídico (AI Lawyer):** Especialista em traduzir termos em latim e jargão jurídico para linguagem clara, apontando prazos, recursos cabíveis e próximos passos.

---

### 📦 4. DEPENDÊNCIAS & BIBLIOTECAS (PYTHON)
Instale as seguintes dependências no ambiente virtual (`venv`):
```bash
pip install reportlab pdfplumber beautifulsoup4
```
*   `reportlab`: Usada para desenhar e renderizar o PDF estruturado com tabelas, cabeçalhos estilizados, numeração de páginas e margens profissionais.
*   `pdfplumber`: Excelente biblioteca para ler PDFs de diários oficiais gigantes, permitindo buscar termos de forma performática e mantendo a formatação tabular das páginas.

---

### 📂 5. SCRIPTS CONSTRUÍDOS
#### 📄 `check_digit.py`
Função que implementa o algoritmo de cálculo do Dígito Verificador padrão CNJ (`NNNNNNN-DD.YYYY.J.TR.OOOO`). Útil para validar se a numeração fornecida pelo cliente está correta antes de iniciar buscas caras.

#### 📄 `search_combo.py` / `find_seq_for_42.py`
Scripts de força bruta/busca que calculam e validam sequências numéricas e comarcas para encontrar o CNJ exato quando há ambiguidade na entrada (por exemplo, quando o usuário fornece um número com dígitos extras ou comarca incorreta).

#### 📄 `generate_report.py`
Gera o arquivo `Relatorio_Executivo_Processo.pdf` utilizando `reportlab`. Implementa tabelas com cores institucionais (Deep Navy/Slate Gray), parágrafos formatados, células auto-ajustáveis para o histórico de decisões da 9ª Câmara Cível (TJMG), e faz a chamada do sistema para abrir o PDF automaticamente (`xdg-open`).

---

### 💬 6. PROMPT MESTRE DE CONSTRUÇÃO (Copiar para iniciar novo projeto)
> "Quero estruturar uma rotina de raspagem e consolidação jurídica:
> 1. Escreva uma função em Python para validar o dígito verificador padrão CNJ (módulo 97) de um processo judicial.
> 2. Use o Playwright para pesquisar o número CNJ na Consulta de 2ª Instância do tribunal selecionado (ex: TJMG) e extrair os dados completos (classe, relator, partes, últimas movimentações).
> 3. Crie um script de busca textual em Diários Oficiais (DJEN) pelo nome da parte ou número do processo usando `pdfplumber`.
> 4. Desenhe um relatório PDF profissional usando a biblioteca `reportlab`. O design deve conter: cabeçalho estilizado, tabela de metadados com as informações estruturadas do processo, tabela de andamentos e histórico de decisões, seção de análise dos próximos passos e fontes. O PDF deve ser gerado em modo paisagem ou retrato profissional de até 5 páginas."

---

### 🚀 7. RECOMENDAÇÕES E EVOLUÇÕES
*   [ ] **Quebra de CAPTCHA:** Integrar bibliotecas como `python-anticaptcha` ou `twocaptcha` para submeter imagens de captcha de portais e-Saj/PJe diretamente para APIs de resolução automática.
*   [ ] **Monitoramento Cron:** Agendar uma rotina semanal usando ferramentas como `cron` ou o MCP scheduler para verificar se há novas movimentações no processo e enviar um resumo consolidado apenas se houver novidades.
*   [ ] **Outros Agentes:** Criar um agente validador de prazos recursais para identificar automaticamente se um despacho abre prazo e alertar a data limite para a contraminuta ou recurso.
