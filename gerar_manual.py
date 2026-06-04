import os
import subprocess
import sys

WORKSPACE = "/home/toten/projeto-antigravity"
TEMP_DIR = os.path.join(WORKSPACE, ".temp")
HTML_FILE = os.path.join(TEMP_DIR, "manual.html")
PDF_FILE = os.path.join(WORKSPACE, "Manual_Avancado_Antigravity.pdf")

os.makedirs(TEMP_DIR, exist_ok=True)

html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Manual de Arquitetura e Operação Avançada - Antigravity</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        @page {
            size: A4;
            margin: 20mm 15mm 20mm 15mm;
            @bottom-right {
                content: counter(page);
            }
        }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #1E293B;
            background-color: #FFFFFF;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            -webkit-print-color-adjust: exact;
        }

        .cover-page {
            page-break-after: always;
            height: 250mm;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding-top: 50mm;
        }

        .cover-title {
            font-family: 'Outfit', sans-serif;
            font-size: 32px;
            font-weight: 800;
            color: #0F172A;
            line-height: 1.2;
            letter-spacing: -1px;
            margin-bottom: 5px;
        }

        .cover-subtitle {
            font-size: 16px;
            color: #0D9488; /* Teal */
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 40mm;
        }

        .cover-details {
            margin-top: auto;
            border-top: 2px solid #E2E8F0;
            padding-top: 20px;
            font-size: 11px;
            color: #64748B;
        }

        .section {
            page-break-inside: avoid;
            margin-bottom: 30px;
        }

        .page-break {
            page-break-before: always;
        }

        h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 20px;
            font-weight: 700;
            color: #0F172A;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 6px;
            margin-top: 30px;
            margin-bottom: 15px;
        }

        h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 15px;
            font-weight: 600;
            color: #0F172A;
            margin-top: 20px;
            margin-bottom: 10px;
        }

        p {
            font-size: 12px;
            margin-top: 0;
            margin-bottom: 12px;
            text-align: justify;
        }

        ul {
            margin-top: 0;
            margin-bottom: 12px;
            padding-left: 20px;
        }

        li {
            font-size: 12px;
            margin-bottom: 5px;
        }

        .code-block {
            font-family: 'JetBrains Mono', monospace;
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 10px;
            color: #334155;
            white-space: pre-wrap;
            word-break: break-all;
            margin-bottom: 15px;
        }

        .highlight-box {
            background-color: #F0FDFA; /* Light Teal background */
            border-left: 4px solid #0D9488;
            padding: 12px 16px;
            border-radius: 0 6px 6px 0;
            margin-bottom: 15px;
        }

        .highlight-box p {
            margin: 0;
            font-size: 11.5px;
            color: #115E59;
        }

        .flow-container {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin: 20px 0;
        }

        .flow-step {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 11px;
        }

        .flow-step-title {
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 3px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
            font-size: 11px;
        }

        th, td {
            border: 1px solid #E2E8F0;
            padding: 8px 10px;
            text-align: left;
        }

        th {
            background-color: #F1F5F9;
            font-weight: 700;
            color: #0F172A;
        }

        .badge {
            display: inline-block;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 9px;
            font-weight: 700;
            text-transform: uppercase;
        }

        .badge-active {
            background-color: #D1FAE5;
            color: #065F46;
        }

        .badge-inactive {
            background-color: #F1F5F9;
            color: #475569;
        }
    </style>
</head>
<body>

    <!-- CAPA -->
    <div class="cover-page">
        <div class="cover-title">MANUAL DE ARQUITETURA E RECUPERAÇÃO AVANÇADA</div>
        <div class="cover-subtitle">Ecossistema Antigravity - Roteamento de Habilidades e Conexões MCP</div>
        
        <div class="highlight-box" style="margin-top: 20mm;">
            <p><strong>Nota de Segurança e Recuperação:</strong> Este documento serve como guia técnico de restauração de estado (recovery) para o caso de perda de contexto do agente, mudança de modelo de IA, ou replicação da estrutura do workspace em outro ambiente.</p>
        </div>

        <div class="cover-details">
            <strong>Ambiente de Execução:</strong> Linux Sandbox (Workspace: <code>/home/toten/projeto-antigravity</code>)<br>
            <strong>Criado em:</strong> 02 de Junho de 2026<br>
            <strong>Versão:</strong> 1.0.0 (Estável)
        </div>
    </div>

    <!-- SEÇÃO 1 -->
    <div class="section">
        <h1>1. Princípios de Design e Saturação de Contexto</h1>
        <p>No desenvolvimento de agentes autônomos baseados em LLMs, dois grandes gargalos degradam o desempenho da IA ao longo do tempo:</p>
        <ul>
            <li><strong>Saturação de Contexto (Prompt Bloat):</strong> Fornecer diretrizes de múltiplos projetos simultaneamente consome tokens desnecessários e aumenta a distração do modelo.</li>
            <li><strong>Poluição de Ferramentas (Tool Overload):</strong> Expor dezenas de ferramentas MCP de banco de dados, busca na web e navegação de uma só vez aumenta a latência e a probabilidade de chamadas erradas ou alucinações.</li>
        </ul>
        <p>A arquitetura implementada resolve esses problemas introduzindo o <strong>acoplamento dinâmico sob demanda</strong>: as diretrizes de comportamento (Skills) e as conexões do sistema (MCPs) são ativadas em tempo real com base no contexto do prompt do usuário, permanecendo em um "Cofre" (Vault) inativo enquanto não são requisitadas.</p>
    </div>

    <!-- SEÇÃO 2 -->
    <div class="section page-break">
        <h1>2. O Cofre de Habilidades (Skills Vault)</h1>
        <p>Habilidades no Antigravity são regras de comportamento escritas em Markdown. O sistema gerencia essas regras em duas pastas:</p>
        <ul>
            <li><code>.agent/skills_vault/</code>: O cofre inativo contendo a biblioteca de habilidades catalogadas.</li>
            <li><code>.agent/skills/</code>: A pasta ativa lida pelo cliente. Contém apenas <strong>links simbólicos (symlinks)</strong> apontando para as pastas do cofre.</li>
        </ul>
        
        <h2>O Script de Orquestração: <code>manage_skills.py</code></h2>
        <p>O script <code style="font-size: 11px;">.agent/manage_skills.py</code> automatiza esse fluxo. Ao receber uma descrição do projeto, ele divide o texto em palavras, compara com as palavras-chave do catálogo JSON e cria ou destrói links simbólicos em tempo real:</p>
        
        <div class="code-block"># Ativação manual
python3 .agent/manage_skills.py activate skill util-brainstorming

# Desativação manual
python3 .agent/manage_skills.py deactivate skill fii-mapear-ri

# Auto-Tune inteligente baseado em contexto
python3 .agent/manage_skills.py auto "Quero consertar um bug no Playwright e rodar no navegador"</div>

        <h2>Visualização de Estado Atual do Catálogo de Habilidades (Resumo)</h2>
        <table>
            <thead>
                <tr>
                    <th>ID da Skill</th>
                    <th>Nome de Exibição</th>
                    <th>Contexto Principal</th>
                    <th>Status Comum</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>fii-mapear-ri</strong></td>
                    <td>Mapear RI e Baixar Relatórios</td>
                    <td>Financeiro (FIIs/Fiagros)</td>
                    <td>Vault / Inativa</td>
                </tr>
                <tr>
                    <td><strong>fii-sintetizar-relatorios</strong></td>
                    <td>Sintetizar Relatórios Financeiros</td>
                    <td>Financeiro (FIIs/Fiagros)</td>
                    <td>Vault / Inativa</td>
                </tr>
                <tr>
                    <td><strong>legal-buscar-processo</strong></td>
                    <td>Buscar Processo Judicial</td>
                    <td>Jurídico (Tribunais/DJE)</td>
                    <td>Vault / Inativa</td>
                </tr>
                <tr>
                    <td><strong>legal-gerar-relatorio</strong></td>
                    <td>Gerar Relatório Jurídico</td>
                    <td>Jurídico (ReportLab PDF)</td>
                    <td>Vault / Inativa</td>
                </tr>
                <tr>
                    <td><strong>util-brainstorming</strong></td>
                    <td>Brainstorming & Design</td>
                    <td>Planejamento / Arquitetura</td>
                    <td>Vault / Inativa</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- SEÇÃO 3 -->
    <div class="section page-break">
        <h1>3. O Portal de Ferramentas (MCP Gateway)</h1>
        <p>O Model Context Protocol (MCP) conecta a IA ao sistema de arquivos, navegadores e barramentos de rede. Em vez de registrar todos os servidores individualmente nas configurações globais do cliente, a arquitetura utiliza o <strong>MCP Gateway</strong>.</p>
        
        <h2>Estrutura de Funcionamento</h2>
        <p>Um único servidor MCP permanente chamado <code>mcp_gateway.py</code> é registrado nas configurações da máquina. Ele age como um proxy de entrada e saída JSON-RPC 2.0:</p>
        
        <div class="flow-container">
            <div class="flow-step">
                <div class="flow-step-title">1. Handshake de Inicialização</div>
                O console do cliente inicia o <code>mcp_gateway.py</code>. O gateway lê o arquivo local <code>.agent/active_mcps.json</code>, inicia os subprocessos dos MCPs filhos ativos e faz o handshake de inicialização individual com cada um.
            </div>
            <div class="flow-step">
                <div class="flow-step-title">2. Mapeamento de Ferramentas</div>
                O cliente solicita a lista de ferramentas (<code>tools/list</code>). O gateway repassa a chamada a todos os filhos ativos, coleta as listas, mapeia os nomes das ferramentas aos respectivos servidores e retorna uma lista unificada ao cliente.
            </div>
            <div class="flow-step">
                <div class="flow-step-title">3. Execução de Ferramenta (Roteamento)</div>
                A IA executa uma ferramenta (<code>tools/call</code>). O gateway intercepta, identifica qual sub-servidor possui a ferramenta, encaminha a chamada para a entrada padrão (stdin) do subprocesso do filho, aguarda a resposta no stdout dele e devolve à IA com a ID original do request.
            </div>
        </div>

        <h2>O Catálogo de Servidores MCP do Gateway</h2>
        <table>
            <thead>
                <tr>
                    <th>ID do Servidor</th>
                    <th>Nome Comercial</th>
                    <th>Comando de Execução</th>
                    <th>Palavras-Chave de Gatilho</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>filesystem</strong></td>
                    <td>Filesystem MCP</td>
                    <td><code>npx -y @modelcontextprotocol/server-filesystem</code></td>
                    <td><em>Sempre ativa (Baseline)</em></td>
                </tr>
                <tr>
                    <td><strong>fetch</strong></td>
                    <td>Fetch MCP</td>
                    <td><code>npx -y @modelcontextprotocol/server-fetch</code></td>
                    <td><em>Sempre ativa (Baseline)</em></td>
                </tr>
                <tr>
                    <td><strong>google-search</strong></td>
                    <td>Google Search MCP</td>
                    <td><code>npx -y @modelcontextprotocol/server-google-search</code></td>
                    <td>busca, google, search, web</td>
                </tr>
                <tr>
                    <td><strong>playwright</strong></td>
                    <td>Playwright MCP</td>
                    <td><code>npx -y @modelcontextprotocol/server-playwright</code></td>
                    <td>playwright, browser, scrape, captcha</td>
                </tr>
                <tr>
                    <td><strong>postgres</strong></td>
                    <td>Postgres MCP</td>
                    <td><code>npx -y @modelcontextprotocol/server-postgres</code></td>
                    <td>postgres, sql, banco, query</td>
                </tr>
                <tr>
                    <td><strong>github</strong></td>
                    <td>GitHub MCP</td>
                    <td><code>npx -y @modelcontextprotocol/server-github</code></td>
                    <td>github, git, pr, branch, issue</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- SEÇÃO 4 -->
    <div class="section page-break">
        <h1>4. Casos de Uso e Projetos de Referência</h1>
        <p>Abaixo estão detalhados os dois projetos principais que fundamentaram essa arquitetura e serviram como provas de conceito (PoC):</p>
        
        <h2>Projeto A: Consolidador de Análise de FIIs & Fiagros</h2>
        <ul>
            <li><strong>Fluxo:</strong> O agente lia tickers em um arquivo de texto, buscava páginas de Relações com Investidores (RI) via Brave/Google Search, baixava PDFs usando o Fetch MCP, extraía texto filtrado com `pypdf` no arquivo `extract_data.py`, gerava um template HTML com CSS altamente polido e renderizava o PDF via Chrome Headless.</li>
            <li><strong>Arquitetura Técnica:</strong>
                <br>- <em>Downloads paralelos:</em> Uso de <code>ThreadPoolExecutor</code> no Python para baixar arquivos de forma assíncrona.
                <br>- <em>Limitação de tokens:</em> Extração limitada a 15k caracteres por PDF baseada em filtragem de palavras-chave para evitar estouro de contexto na IA.
            </li>
        </ul>

        <h2>Projeto B: Robô de Pesquisa Processual (TJMG & DJEN)</h2>
        <ul>
            <li><strong>Fluxo:</strong> Validação do dígito verificador CNJ de um processo judicial por módulo 97, raspagem automatizada na 2ª instância do portal do TJMG, análise de captchas em tela para resolução manual/assistida, cruzamento de dados com publicações do Diário de Justiça Eletrônico Nacional (DJEN) e compilação do andamento em um PDF executivo usando ReportLab.</li>
            <li><strong>Arquitetura Técnica:</strong>
                <br>- <em>Validação Algorítmica:</em> O script <code>check_digit.py</code> realizava a validação numérica para economizar processamento e descartar consultas inválidas de imediato.
                <br>- <em>Força bruta de Comarca:</em> O script <code>search_combo.py</code> buscava no portal a combinação certa de sequência e comarca que resultasse no dígito verificador fornecido quando havia ambiguidade de digitação.
            </li>
        </ul>
    </div>

    <!-- SEÇÃO 5 -->
    <div class="section page-break">
        <h1>5. Fluxo de Execução de um Prompt (Passo a Passo)</h1>
        <p>Quando o usuário interage com o agente, o ciclo de vida completo do processamento de uma tarefa segue a seguinte ordem:</p>
        
        <div class="flow-container">
            <div class="flow-step">
                <div class="flow-step-title">1. Entrada do Usuário</div>
                O usuário envia a mensagem com o objetivo do projeto (ex: "Agy, quero analisar a carteira de FIIs e exportar").
            </div>
            <div class="flow-step">
                <div class="flow-step-title">2. Auto-Tunning Dinâmico (skills e mcps)</div>
                O agente intercepta a intenção e executa o script local <code>manage_skills.py auto "<frase>"</code>. As skills necessárias viram symlinks ativos e os MCPs necessários são escritos em <code>active_mcps.json</code>.
            </div>
            <div class="flow-step">
                <div class="flow-step-title">3. Re-inicialização do Gateway</div>
                Na próxima chamada de ferramenta da sessão, o gateway identifica a alteração de estado dos servidores MCP ativos, encerra as conexões inativas antigas e inicializa as novas conexões.
            </div>
            <div class="flow-step">
                <div class="flow-step-title">4. Execução da Tarefa e Verificação</div>
                O agente executa o código ou automação usando apenas o conjunto estrito de ferramentas permitidas, reduzindo o tempo de processamento e garantindo estabilidade máxima.
            </div>
        </div>
    </div>

    <!-- SEÇÃO 6 -->
    <div class="section page-break">
        <h1>6. Manual de Recuperação e Replicação (Prompt Mestre)</h1>
        <p>Caso o agente sofra uma perda de memória completa, ou caso você configure um novo ambiente do zero, copie e cole o prompt mestre de bootstrap abaixo no chat da nova IA para reestruturar todo este ecossistema automaticamente:</p>
        
        <div class="code-block" style="font-size: 9px; line-height: 1.4;">"Quero estruturar meu workspace com um sistema dinâmico de Habilidades (Skills) e Servidores MCP sob demanda.

1. Crie uma pasta '.agent/' contendo as subpastas 'skills/', 'skills_vault/' e o arquivo de catálogo 'skills_catalog.json'.
2. Desenhe um script Python '.agent/manage_skills.py' com suporte a:
   - 'list': lista skills do vault e MCPs do catálogo global.
   - 'activate/deactivate': cria/remove links simbólicos da skill da pasta vault para a pasta ativa 'skills/'.
   - 'auto <query>': compara as palavras-chave do catálogo com a frase de entrada, ativando skills e escrevendo os MCPs correspondentes em '.agent/active_mcps.json'.
3. Crie um arquivo de catálogo de MCPs '.agent/mcp_catalog.json' contendo definições para 'filesystem', 'fetch', 'google-search', 'playwright', 'postgres' e 'github'.
4. Crie um servidor roteador assíncrono '.agent/mcp_gateway.py' em Python (JSON-RPC stdio proxy) que inicia os subprocessos dos MCPs contidos em '.agent/active_mcps.json', repassa as requisições de ferramentas ('tools/list' e 'tools/call') e devolve a resposta.
5. Instrua-me a cadastrar apenas o 'mcp_gateway.py' nas configurações de mcpServers do console principal do cliente."</div>
    </div>

</body>
</html>
"""

# Write HTML file
with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Generated HTML template at {HTML_FILE}")

# Convert to PDF using Google Chrome
try:
    print(f"Printing manual HTML to PDF at {PDF_FILE}...")
    chrome_cmd = [
        "/usr/bin/google-chrome",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={PDF_FILE}",
        f"file://{HTML_FILE}"
    ]
    subprocess.run(chrome_cmd, check=True)
    print(f"Successfully generated PDF Manual at: {PDF_FILE}")
    
    # Open PDF automatically on user desktop
    try:
        subprocess.run(["xdg-open", PDF_FILE], check=True)
        print("Opened PDF automatically on user desktop.")
    except Exception as e:
        print(f"Could not open PDF: {e}")
except Exception as e:
    print(f"Failed to generate PDF via google-chrome: {e}")
    sys.exit(1)
