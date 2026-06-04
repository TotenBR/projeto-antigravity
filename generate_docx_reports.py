import os
import sys

# Install python-docx if not installed
try:
    import docx
except ImportError:
    print("Installing python-docx...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "python-docx"], check=True)
    import docx

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=200, right=200):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_code_block(doc, text):
    table = doc.add_table(rows=1, cols=1)
    cell = table.cell(0, 0)
    set_cell_shading(cell, "F8FAFC")
    set_cell_margins(cell)
    
    # Remove table borders
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for b in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        node = OxmlElement(f'w:{b}')
        node.set(qn('w:val'), 'none')
        tblBorders.append(node)
    tblPr.append(tblBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    
    run = p.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(51, 65, 85) # Slate

def create_fii_document(output_path):
    doc = Document()
    
    # Page setup
    for section in doc.sections:
        section.top_margin = Pt(72)
        section.bottom_margin = Pt(72)
        section.left_margin = Pt(72)
        section.right_margin = Pt(72)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    
    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(12)
    run_title = p_title.add_run("📊 PROJETO FIIs & FIAGROS - Automação e Consolidação")
    run_title.font.bold = True
    run_title.font.size = Pt(20)
    run_title.font.color.rgb = RGBColor(13, 148, 136) # Teal
    
    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(20)
    run_sub = p_sub.add_run("Manual de Referência Técnica para Construção, Prompts e Dependências")
    run_sub.font.size = Pt(11)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(100, 116, 139)
    
    def add_section_header(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.font.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(13, 148, 136)
        
    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        if bold_prefix:
            run_prefix = p.add_run(bold_prefix)
            run_prefix.bold = True
        p.add_run(text)
        
    # Content
    add_section_header("📌 1. OBJETIVO DO PROJETO")
    doc.add_paragraph("Buscar na internet de forma autônoma relatórios gerenciais/mensais (PDFs) de uma lista de fundos imobiliários (FIIs/Fiagros), extrair trechos importantes (focando em riscos, vacância e alocação) e consolidar os dados em um relatório executivo PDF altamente profissional.")
    
    add_section_header("⚙️ 2. SERVIDORES MCP (INFRAESTRUTURA)")
    add_bullet(" Para localizar as páginas de RI de cada fundo via busca web em tempo real.", "Google Search MCP:")
    add_bullet(" Para acessar URLs de Relações com Investidores e inicializar o download de arquivos PDF.", "Fetch MCP:")
    add_bullet(" Para ler a lista inicial de ativos (LISTA DE FIIS.txt) e salvar o relatório PDF final no HD.", "Filesystem MCP:")
    
    add_section_header("📦 3. DEPENDÊNCIAS & BIBLIOTECAS (PYTHON)")
    doc.add_paragraph("Instale as seguintes dependências no ambiente virtual (venv):")
    add_code_block(doc, "pip install beautifulsoup4 pypdf reportlab")
    
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.add_run("Detalhamento de uso das bibliotecas:").italic = True
    add_bullet(" Usada para fazer o parsing dos resultados das páginas de busca e extrair links dos PDFs.", "beautifulsoup4 (bs4):")
    add_bullet(" Usada para abrir os relatórios baixados, fazer buscas por termos-chave e extrair o texto de páginas relevantes.", "pypdf:")
    add_bullet(" Utilizado em conjunto com o Google Chrome Headless para criar layouts visuais com CSS moderno e exportá-los em PDF com design de alto nível.", "HTML/CSS + Headless Chrome:")

    add_section_header("🤖 4. HABILIDADES DO AGENTE (AGENT SKILLS)")
    doc.add_paragraph("Habilidades configuradas no diretório /.agent/skills/ para guiar a IA na execução padrão:")
    add_bullet(" Busca os sites de RI, identifica os relatórios mais recentes e realiza o download para a pasta temporária `/.temp/`.", "Skill 1: /mapear-ri (/.agent/skills/mapear-ri/agent/skill.md) -")
    add_bullet(" Analisa os PDFs baixados, extrai pontos críticos (vacância, alavancagem, inadimplência) e compila o relatório PDF final.", "Skill 2: /sintetizar-relatorios (/.agent/skills/sintetizar-relatorios/agent/skill.md) -")

    add_section_header("📂 5. SCRIPTS CONSTRUÍDOS")
    add_bullet(" Gerencia a busca concorrente no Yahoo Search por relatórios dos fundos. Utiliza ThreadPoolExecutor para baixar múltiplos arquivos em paralelo e valida os arquivos verificando a assinatura digital `%PDF`.", "mapear_ri.py -")
    add_bullet(" Abre os arquivos baixados usando pypdf, lê as 3 primeiras páginas e escaneia o restante do texto por palavras-chave relevantes. Limita a saída a 15k caracteres por relatório e gera o arquivo JSON intermediário `extracted_text.json`.", "extract_data.py -")
    add_bullet(" Consome as informações do JSON e monta um relatório HTML consolidado estruturado com CSS avançado. Possui suporte a badges coloridos de alerta e executa o comando `google-chrome --headless --print-to-pdf` para gerar o documento final.", "gerar_pdf.py -")

    add_section_header("💬 6. PROMPT MESTRE PARA REPRODUÇÃO")
    doc.add_paragraph("Copie o prompt abaixo em um novo chat para recriar todo este projeto do zero:")
    prompt_text = (
        "Quero criar uma automação em Python para análise de Fundos Imobiliários.\n"
        "1. Leia um arquivo LISTA DE FIIS.txt contendo tickers (um por linha).\n"
        "2. Faça buscas na web para encontrar e baixar os 2 relatórios gerenciais mais recentes de cada fundo em formato PDF para uma pasta .temp/.\n"
        "3. Crie um script de extração usando pypdf para minerar dados focando em 'vacância', 'inadimplência', 'alavancagem', 'comentários do gestor' e 'dividendos'. Limite o contexto extraído por arquivo.\n"
        "4. Crie um script que compile estes dados em uma página HTML visualmente atraente (com visual moderno, badges de cores para riscos/alertas) e converta em PDF executivo consolidado usando o Google Chrome em modo headless."
    )
    add_code_block(doc, prompt_text)

    add_section_header("🚀 7. RECOMENDAÇÕES DE EVOLUÇÃO")
    add_bullet(" Criar um agente secundário especialista em macroeconomia para ler notícias de juros (Selic, IPCA) e prever impactos nos rendimentos dos fundos.", "Agente de Análise Macroeconômica (MacroAI):")
    add_bullet(" Utilizar a biblioteca pdfplumber se precisar de extrações mais precisas de tabelas financeiras complexas.", "pdfplumber para tabelas:")
    add_bullet(" Configurar um script para enviar o PDF gerado diretamente para o seu Telegram ou e-mail de forma automática.", "Notificação:")

    doc.save(output_path)
    print(f"FIIs docx created at {output_path}")

def create_legal_document(output_path):
    doc = Document()
    
    # Page setup
    for section in doc.sections:
        section.top_margin = Pt(72)
        section.bottom_margin = Pt(72)
        section.left_margin = Pt(72)
        section.right_margin = Pt(72)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    
    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(12)
    run_title = p_title.add_run("⚖️ PROJETO PESQUISA PROCESSUAL - TJMG & DJEN")
    run_title.font.bold = True
    run_title.font.size = Pt(20)
    run_title.font.color.rgb = RGBColor(217, 119, 6) # Orange
    
    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(20)
    run_sub = p_sub.add_run("Manual de Referência Técnica para Busca Processual e Geração de Relatórios")
    run_sub.font.size = Pt(11)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(100, 116, 139)
    
    def add_section_header(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.font.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(217, 119, 6)
        
    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        if bold_prefix:
            run_prefix = p.add_run(bold_prefix)
            run_prefix.bold = True
        p.add_run(text)
        
    # Content
    add_section_header("📌 1. OBJETIVO DO PROJETO")
    doc.add_paragraph("Pesquisar andamentos, decisões e publicações de um processo judicial específico em portais de tribunais (como o TJMG) e diários oficiais (DJEN/DJE), tratar inconsistências de numeração única CNJ e gerar um Relatório Jurídico Executivo profissional de até 5 páginas.")
    
    add_section_header("⚙️ 2. SERVIDORES MCP (INFRAESTRUTURA)")
    add_bullet(" Essencial para navegar em portais de tribunais dinâmicos (renderização de JS, preenchimento de formulários, cliques e extração de dados).", "Puppeteer MCP / Playwright MCP:")
    add_bullet(" Para visualização em tempo real das páginas do tribunal para resolução de captchas manuais pelo usuário.", "Browser / Screenshot MCP:")
    add_bullet(" Para manipulação de arquivos locais e armazenamento dos relatórios em PDF.", "Filesystem MCP:")
    
    add_section_header("🤖 3. ARQUITETURA DE AGENTES JURÍDICOS (SUGESTÃO)")
    add_bullet(" JurisBot (Agente Paralegal): Entende a estrutura de busca de sistemas como e-Saj, PJe ou PROJUDI.", "Agente Paralegal de Consulta:")
    add_bullet(" ClippingBot (Agente de Pesquisa Pública): Especializado em varrer diários eletrônicos (DJE/DJEN) e extrair citações ao processo.", "Agente de Clipping:")
    add_bullet(" AI Lawyer (Consultor Jurídico): Traduz andamentos técnicos para linguagem de negócios, mapeando prazos e riscos.", "Agente Consultor Jurídico:")
    
    add_section_header("📦 4. DEPENDÊNCIAS & BIBLIOTECAS (PYTHON)")
    doc.add_paragraph("Instale as seguintes dependências no ambiente virtual (venv):")
    add_code_block(doc, "pip install reportlab pdfplumber beautifulsoup4")
    
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.add_run("Detalhamento de uso das bibliotecas:").italic = True
    add_bullet(" Utilizado para gerar o layout profissional em PDF de forma programática.", "reportlab:")
    add_bullet(" Utilizado para buscas rápidas de strings dentro de grandes PDFs de Diários Oficiais.", "pdfplumber:")

    add_section_header("📂 5. SCRIPTS CONSTRUÍDOS")
    add_bullet(" Implementa o algoritmo de cálculo do Dígito Verificador padrão CNJ (módulo 97) para validar o número do processo antes de iniciar as buscas.", "check_digit.py -")
    add_bullet(" Scripts de busca para validar comarcas e sequências que resultam no dígito verificador 42, útil para solucionar números CNJ incompletos ou digitados incorretamente.", "search_combo.py / find_seq_for_42.py -")
    add_bullet(" Gera o Relatório_Executivo_Processo.pdf utilizando a biblioteca ReportLab, com tabelas estilizadas, histórico de decisões e análise de riscos.", "generate_report.py -")

    add_section_header("💬 6. PROMPT MESTRE PARA REPRODUÇÃO")
    doc.add_paragraph("Copie o prompt abaixo em um novo chat para recriar todo este projeto do zero:")
    prompt_text = (
        "Quero estruturar uma rotina de raspagem e consolidação jurídica:\n"
        "1. Escreva uma função em Python para validar o dígito verificador padrão CNJ (módulo 97) de um processo judicial.\n"
        "2. Use o Playwright para pesquisar o número CNJ na Consulta de 2ª Instância do tribunal selecionado (ex: TJMG) e extrair os dados completos (classe, relator, partes, últimas movimentações).\n"
        "3. Crie um script de busca textual em Diários Oficiais (DJEN) pelo nome da parte ou número do processo usando pdfplumber.\n"
        "4. Desenhe um relatório PDF profissional usando a biblioteca reportlab. O design deve conter: cabeçalho estilizado, tabela de metadados com as informações estruturadas do processo, tabela de andamentos e histórico de decisões, seção de análise dos próximos passos e fontes. O PDF deve ser gerado em modo paisagem ou retrato profissional de até 5 páginas."
    )
    add_code_block(doc, prompt_text)

    add_section_header("🚀 7. RECOMENDAÇÕES DE EVOLUÇÃO")
    add_bullet(" Integrar bibliotecas como python-anticaptcha ou twocaptcha para submeter imagens de captcha de forma automática via API.", "Quebra de CAPTCHA:")
    add_bullet(" Agendar rotinas semanais para checar novos andamentos e gerar relatórios executivos de atualização apenas se houver novidades.", "Monitoramento Cron:")
    add_bullet(" Identificar prazos abertos por intimação e calcular a data limite para recursos de forma autônoma.", "Agente Validador de Prazos:")

    doc.save(output_path)
    print(f"Legal docx created at {output_path}")

if __name__ == "__main__":
    workspace = "/home/toten/projeto-antigravity"
    fii_path = os.path.join(workspace, "Relatorio_FIIs.docx")
    legal_path = os.path.join(workspace, "Relatorio_Pesquisa_Processual.docx")
    create_fii_document(fii_path)
    create_legal_document(legal_path)
    print("All docx files generated successfully.")
