import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# Define custom canvas for "Page X of Y" and running headers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Page 1 is the cover, do not draw headers/footers
        if self._pageNumber == 1:
            # Draw elegant cover background graphics
            self.saveState()
            # Deep Navy sidebar
            self.setFillColor(colors.HexColor("#0B2545"))
            self.rect(0, 0, 35, 841.89, fill=True, stroke=False)
            # Gold accent line
            self.setFillColor(colors.HexColor("#D4AF37"))
            self.rect(35, 0, 6, 841.89, fill=True, stroke=False)
            self.restoreState()
            return

        self.saveState()

        # Draw Running Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0B2545"))
        self.drawString(54, 800, "RELATÓRIO EXECUTIVE DE INVESTIMENTOS | DEPARTAMENTO DE ANÁLISE (CNPI)")
        self.setFont("Helvetica", 8)
        self.drawRightString(541, 800, "PORTFÓLIO DE ATIVOS FIIs, FIAGROs E FI-INFRA")
        self.setStrokeColor(colors.HexColor("#D4AF37"))
        self.setLineWidth(0.75)
        self.line(54, 792, 541, 792)

        # Draw Running Footer
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0B2545"))
        self.drawString(54, 36, "CONFIDENCIAL")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#2E3033"))
        self.drawString(135, 36, "|   USO EXCLUSIVO E PESSOAL")
        
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(541, 36, page_text)
        self.setStrokeColor(colors.HexColor("#EEF4F8"))
        self.setLineWidth(0.5)
        self.line(54, 48, 541, 48)

        self.restoreState()


def build_pdf():
    # Setup document
    pdf_path = "/fii_analysis/relatorio_fii_executivo.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,   # Leave space for running header
        bottomMargin=72 # Leave space for running footer
    )

    styles = getSampleStyleSheet()

    # Define custom styles
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.HexColor('#0B2545'),
        alignment=TA_CENTER
    )

    cover_subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2E3033'),
        alignment=TA_CENTER
    )

    cover_metadata_style = ParagraphStyle(
        'CoverMetadata',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#2E3033')
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#0B2545'),
        spaceAfter=12,
        spaceBefore=14,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#D4AF37'),
        spaceAfter=6,
        spaceBefore=10,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#2E3033'),
        spaceAfter=8
    )

    body_justify = ParagraphStyle(
        'BodyJustify',
        parent=body_style,
        alignment=TA_JUSTIFY,
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#2E3033'),
        spaceAfter=4
    )

    cell_style_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#0B2545'),
        alignment=TA_CENTER
    )

    cell_style_normal = ParagraphStyle(
        'CellNormal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#2E3033'),
        alignment=TA_CENTER
    )

    # Pill styles for projections/recommendations
    reco_compra = ParagraphStyle(
        'RecoCompra',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#2A7B4C'),
        alignment=TA_LEFT
    )

    reco_manutencao = ParagraphStyle(
        'RecoManutencao',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#D97706'),
        alignment=TA_LEFT
    )

    reco_venda = ParagraphStyle(
        'RecoVenda',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#C2410C'),
        alignment=TA_LEFT
    )

    story = []

    # ================= PAGE 1: COVER PAGE =================
    story.append(Spacer(1, 120))
    story.append(Paragraph("<font color='#D4AF37'><b>DEPARTAMENTO DE INTELIGÊNCIA FINANCEIRA</b></font>", ParagraphStyle('CoverPre', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=colors.HexColor('#D4AF37'), alignment=TA_CENTER)))
    story.append(Spacer(1, 15))
    story.append(Paragraph("RELATÓRIO DE INTELIGÊNCIA<br/>DE MERCADO E ALOCAÇÃO DE ATIVOS", cover_title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Análise Fundamentalista Crítica, Projeções de Longo Prazo e Recomendações Táticas para FIIs, FIAGROs e FI-Infra", cover_subtitle_style))
    story.append(Spacer(1, 40))

    # Elegant horizontal gold bar
    gold_bar_data = [[""]]
    gold_bar_table = Table(gold_bar_data, colWidths=[200])
    gold_bar_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#D4AF37')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(gold_bar_table)
    story.append(Spacer(1, 160))

    # Metadata Card (Table)
    metadata_data = [
        [
            Paragraph("<b>Preparado por:</b> Analista Sênior Credenciado (CNPI)", cover_metadata_style),
            Paragraph("<b>Data de Emissão:</b> Junho de 2026", cover_metadata_style)
        ],
        [
            Paragraph("<b>Público-Alvo:</b> Clientes Private & Investidores Qualificados", cover_metadata_style),
            Paragraph("<b>Status do Documento:</b> Oficial / Confidencial", cover_metadata_style)
        ]
    ]
    metadata_table = Table(metadata_data, colWidths=[240, 240])
    metadata_table.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 0.5, colors.HexColor('#D4AF37')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(metadata_table)
    story.append(PageBreak())

    # ================= PAGE 2: MACROECONOMIC OUTLOOK =================
    story.append(Paragraph("PANORAMA MACROECONÔMICO & DIRETRIZES DE INVESTIMENTO", h1_style))
    story.append(Spacer(1, 10))

    macro_p1 = (
        "O cenário macroeconômico brasileiro em meados de 2026 apresenta desafios decorrentes de pressões inflacionárias persistentes, "
        "com a expectativa do IPCA para o encerramento do ano elevada a 5.09% segundo o Boletim Focus de junho. Para mitigar esse risco, "
        "o Banco Central mantém a taxa Selic em patamar restritivo de 14.50% ao ano, após um longo período de estabilidade em 15.00% que se estendeu até março. "
        "As projeções de mercado (Focus) apontam para cortes graduais até 13.25% ao final de 2026 e 11.25% em 2027. "
        "A manutenção de juros altos por mais tempo beneficia e sustenta yields elevados em ativos de papel e crédito (CRI, CRA, Debêntures), "
        "enquanto o início do ciclo de cortes sinaliza uma assimetria de valorização relevante para os ativos de tijolo de alta qualidade (AAA) no médio prazo."
    )
    story.append(Paragraph(macro_p1, body_style))

    macro_p2 = (
        "<b>Setor de Tijolo (Logística, Shoppings e Renda Urbana):</b> Apresenta um ponto de entrada altamente favorável. "
        "Com a queda das taxas futuras de juros, ativos de alta qualidade técnica (AAA) com contratos de longo prazo "
        "indexados à inflação (IPCA) tendem a apresentar forte valorização de cota patrimonial. O segmento logístico mostra vacância sob controle "
        "nas regiões 'last mile' e o setor de shopping centers premium continua colhendo recordes de vendas dos lojistas, repassando o reajuste nos aluguéis mínimos."
    )
    story.append(Paragraph(macro_p2, body_style))

    macro_p3 = (
        "<b>Setor de Papel (Recebíveis Imobiliários, FIAGROs e FI-Infra):</b> Cumpre um papel tático indispensável em carteiras "
        "de investimento, gerando fluxos mensais isentos de imposto de renda e de alta previsibilidade. Com taxas reais médias de carrego de "
        "IPCA + 7% e CDI + 2.5%, os fundos de papel protegem o portfólio contra oscilações de mercado e sustentam yields elevados. "
        "No entanto, em meados de 2026, a seleção rigorosa de crédito (high grade) é crucial, uma vez que o estresse pontual no agronegócio "
        "e em devedores menos estruturados demanda portfólios maduros com garantias imobiliárias robustas."
    )
    story.append(Paragraph(macro_p3, body_style))

    story.append(Spacer(1, 15))
    story.append(Paragraph("INDICADORES MACROECONÔMICOS E PREMISSAS DE MODELO", h2_style))

    # Macro Indicators Table
    macro_table_data = [
        [
            Paragraph("<b>Indicador de Mercado</b>", cell_style_bold),
            Paragraph("<b>Patamar Atual (2026)</b>", cell_style_bold),
            Paragraph("<b>Projeção Longo Prazo</b>", cell_style_bold),
            Paragraph("<b>Impacto Alocação FIIs</b>", cell_style_bold)
        ],
        [
            Paragraph("Taxa Selic", cell_style_normal),
            Paragraph("14.50% a.a.", cell_style_normal),
            Paragraph("13.25% a.a. (fim 2026) / 11.25% a.a. (fim 2027)", cell_style_normal),
            Paragraph("Positivo para Tijolo / Redução marginal de ganho em Papel (CDI)", cell_style_normal)
        ],
        [
            Paragraph("IPCA (Inflação)", cell_style_normal),
            Paragraph("5.09% a.a.", cell_style_normal),
            Paragraph("4.02% a.a. (fim de 2027)", cell_style_normal),
            Paragraph("Estabilização do poder de compra e indexação saudável de CRIs/CRAs", cell_style_normal)
        ],
        [
            Paragraph("Índice IFIX", cell_style_normal),
            Paragraph("3.420 pontos", cell_style_normal),
            Paragraph("Tendência Altista", cell_style_normal),
            Paragraph("Fluxo de captação de recursos retornando para emissões líquidas", cell_style_normal)
        ],
        [
            Paragraph("Spread de Crédito", cell_style_normal),
            Paragraph("NTN-B + 6.20%", cell_style_normal),
            Paragraph("Compressão marginal", cell_style_normal),
            Paragraph("Geração de prêmio real elevado em ativos de infraestrutura", cell_style_normal)
        ]
    ]
    macro_table = Table(macro_table_data, colWidths=[100, 100, 110, 170])
    macro_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0B2545')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D4AF37')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    # Overwrite the text color for table headers in macro table
    for i in range(4):
        macro_table_data[0][i].style.textColor = colors.white

    story.append(macro_table)
    story.append(PageBreak())

    # ================= PAGES 3-11: 18 ASSETS (2 per page) =================
    assets_data = [
        {
            "ticker": "HGLG11",
            "nome": "CSHG Logística (Pátria Log)",
            "segmento": "Logística (Tijolo)",
            "preco_atual": "R$ 154,19",
            "vpa": "R$ 153,50",
            "pvp": "1.00",
            "dy_12m": "8.6%",
            "ultimo_div": "R$ 1,10",
            "proj_preco": "Subir",
            "proj_div": "Manter",
            "reco": "Compra",
            "just_preco": "O fundo possui galpões de altíssima qualidade (AAA) em regiões metropolitanas estratégicas. Com a queda gradual dos juros de longo prazo e a resiliência do setor logístico, a taxa de capitalização tende a comprimir, elevando o valor de mercado das cotas.",
            "just_div": "A receita de locação é altamente estável com contratos de longo prazo reajustados pelo IPCA. O yield deve se manter robusto no patamar de R$ 1,10 por cota, com possibilidade de distribuições não recorrentes no final do semestre por ganhos de capital em vendas imobiliárias.",
            "reco_detalhe": "Excelente histórico de gestão da Pátria (ex-CSHG). Peso sugerido de 8.0% na carteira consolidada pelo balanço exemplar de risco e retorno."
        },
        {
            "ticker": "XPML11",
            "nome": "XP Malls FII",
            "segmento": "Shopping Centers (Tijolo)",
            "preco_atual": "R$ 106,57",
            "vpa": "R$ 110,51",
            "pvp": "0.96",
            "dy_12m": "10.3%",
            "ultimo_div": "R$ 0,92",
            "proj_preco": "Subir",
            "proj_div": "Subir",
            "reco": "Compra",
            "just_preco": "Negociando com desconto atrativo sobre o valor patrimonial de tijolo. A consolidação de portfólio dominante em shoppings de alta renda e a maturação das últimas aquisições dão sustentação para ganho de capital significativo à medida que o consumo de luxo se consolida.",
            "just_div": "As vendas dos lojistas continuam a registrar crescimento robusto acima da inflação. A estrutura de aluguel percentual e o repasse inflacionário nos aluguéis mínimos devem impulsionar a distribuição de proventos para patamares ainda maiores no curto prazo.",
            "reco_detalhe": "O setor de shoppings premium é o mais defensivo do varejo físico. Recomendamos Compra com peso sugerido de 7.5% no portfólio consolidado."
        },
        {
            "ticker": "MXRF11",
            "nome": "Maxi Renda FII",
            "segmento": "Recebíveis (Papel)",
            "preco_atual": "R$ 9,85",
            "vpa": "R$ 9,90",
            "pvp": "1.00",
            "dy_12m": "12.1%",
            "ultimo_div": "R$ 0,10",
            "proj_preco": "Manter",
            "proj_div": "Manter",
            "reco": "Manutenção",
            "just_preco": "Ativo muito popular negociado próximo ao seu valor de face patrimonial. Por ser um fundo de papel com grande liquidez, a cota de mercado tende a flutuar em bandas estreitas ao redor de R$ 9,80 - R$ 10,20, sem grande espaço para valorização expressiva.",
            "just_div": "A carteira de CRIs está bem indexada ao CDI e IPCA (taxas médias saudáveis de inflação + 7.5% e CDI + 2.5%). Esperamos estabilidade nos proventos de R$ 0,10 por cota por conta da manutenção da taxa Selic em patamar de dois dígitos.",
            "reco_detalhe": "Recomendamos Manutenção. O ativo cumpre papel essencial de geração de caixa regular e liquidez extrema para a carteira. Alocação recomendada de 6.0%."
        },
        {
            "ticker": "KNRI11",
            "nome": "Kinea Renda Imobiliária",
            "segmento": "Híbrido (Lajes/Logística)",
            "preco_atual": "R$ 158,28",
            "vpa": "R$ 163,43",
            "pvp": "0.97",
            "dy_12m": "8.3%",
            "ultimo_div": "R$ 1,10",
            "proj_preco": "Subir",
            "proj_div": "Manter",
            "reco": "Compra",
            "just_preco": "Desconto de 3% sobre o patrimônio de tijolos de altíssimo padrão da Kinea. A retomada das lajes corporativas premium em São Paulo e o baixo nível de vacância do portfólio logístico abrem espaço para valorização patrimonial das cotas.",
            "just_div": "A taxa de vacância física está sob forte controle (abaixo de 3%). O rendimento mensal de R$ 1,10 é sustentado por contratos de longo prazo com devedores e inquilinos de primeira linha, garantindo estabilidade absoluta para o caixa do cotista.",
            "reco_detalhe": "Compra defensiva de altíssima qualidade. Perfeito para investidores institucionais e conservadores. Peso recomendado de 7.5% no portfólio."
        },
        {
            "ticker": "BRCO11",
            "nome": "Bresco Logística FII",
            "segmento": "Logística (Tijolo)",
            "preco_atual": "R$ 116,02",
            "vpa": "R$ 116,02",
            "pvp": "1.00",
            "dy_12m": "9.2%",
            "ultimo_div": "R$ 0,89",
            "proj_preco": "Subir",
            "proj_div": "Manter",
            "reco": "Compra",
            "just_preco": "O portfólio do fundo possui especificações técnicas excepcionais (AAA) com localização 'last mile' premium em São Paulo. A alta qualidade dos inquilinos (Mercado Livre, GPA, DHL) reduz o risco de crédito e sustenta o valor real dos ativos.",
            "just_div": "A vacância de 7.7% e os contratos atípicos (38% da receita) com prazo médio de 4.9 anos oferecem excelente previsibilidade de receitas. Esperamos manutenção do patamar de distribuição de R$ 0,89 com ajustes inflacionários graduais.",
            "reco_detalhe": "Um dos melhores veículos de logística do mercado nacional. Recomendamos Compra com peso sugerido de 6.5% na carteira de FIIs."
        },
        {
            "ticker": "LVBI11",
            "nome": "VBI Logístico FII",
            "segmento": "Logística (Tijolo)",
            "preco_atual": "R$ 105,42",
            "vpa": "R$ 120,34",
            "pvp": "0.88",
            "dy_12m": "8.5%",
            "ultimo_div": "R$ 0,75",
            "proj_preco": "Subir",
            "proj_div": "Subir",
            "reco": "Compra",
            "just_preco": "Forte desconto patrimonial de 12% (P/VP de 0.88), o que é injustificado para a qualidade dos ativos logísticos da VBI. À medida que as taxas de juros futuras caírem, a distorção de preço deve ser corrigida rapidamente.",
            "just_div": "Com as recentes aquisições de ativos prontos e locados com contratos de longo prazo, a receita recorrente aumentará, permitindo uma elevação da distribuição mensal de proventos de R$ 0,75 para patamares superiores nos próximos trimestres.",
            "reco_detalhe": "Compra altamente recomendada pelo expressivo deságio de 12%. Excelente oportunidade de ganho de capital. Peso sugerido de 5.5%."
        },
        {
            "ticker": "HGRU11",
            "nome": "Pátria Renda Urbana FII",
            "segmento": "Renda Urbana (Tijolo)",
            "preco_atual": "R$ 128,87",
            "vpa": "R$ 128,87",
            "pvp": "1.00",
            "dy_12m": "9.6%",
            "ultimo_div": "R$ 0,85",
            "proj_preco": "Subir",
            "proj_div": "Manter",
            "reco": "Compra",
            "just_preco": "O fundo de renda urbana mais consolidado do mercado. O portfólio consiste em supermercados (Carrefour, GPA) e instituições de ensino (Kroton). A reciclagem ativa de carteira gera ganho de capital consistente e protege o valor de mercado.",
            "just_div": "Os dividendos são muito estáveis pelo perfil atípico dos contratos de locação. A gestão tem excelente histórico de desinvestimento com lucro imobiliário, o que continuará suportando dividendos robustos no patamar atual de R$ 0,85.",
            "reco_detalhe": "Compra para portfólios focados em renda resiliente e de baixo risco de crédito. Alocação recomendada de 7.0%."
        },
        {
            "ticker": "TVRI11",
            "nome": "Tivio Renda Imobiliária FII",
            "segmento": "Agências Bancárias (Tijolo)",
            "preco_atual": "R$ 90,50",
            "vpa": "R$ 95,26",
            "pvp": "0.95",
            "dy_12m": "13.5%",
            "ultimo_div": "R$ 1,05",
            "proj_preco": "Manter",
            "proj_div": "Cair",
            "reco": "Venda",
            "just_preco": "O fundo (ex-BBPO11) possui contratos de locação atípicos com o Banco do Brasil que começam a vencer nos próximos anos. Embora as agências sejam essenciais, há risco real de desocupação ou renegociação de aluguel por valores de mercado muito inferiores.",
            "just_div": "A alta distribuição atual de R$ 1,05 por cota (DY de 13.5%) reflete contratos antigos em patamares acima do mercado. À medida que os vencimentos se aproximarem, a incerteza pressionará as cotas e a receita sofrerá com revisões negativas.",
            "reco_detalhe": "Recomendamos Venda ou Redução estratégica para evitar o risco locatício do setor de agências físicas bancárias no longo prazo. Peso: 0.0%."
        },
        {
            "ticker": "SNAG11",
            "nome": "Suno Agro FIAGRO",
            "segmento": "FIAGRO (Crédito)",
            "preco_atual": "R$ 10,10",
            "vpa": "R$ 10,08",
            "pvp": "1.00",
            "dy_12m": "12.5%",
            "ultimo_div": "R$ 0,105",
            "proj_preco": "Manter",
            "proj_div": "Manter",
            "reco": "Manutenção",
            "just_preco": "O ativo de agronegócio da Suno é gerido de forma muito prudente e focado em crédito para cooperativas e produtores de grande porte. Negociado ao preço justo, o foco é a estabilidade de capital, com pouca oscilação de preço.",
            "just_div": "A carteira é composta majoritariamente por CRAs indexados ao CDI + spread saudável. Esperamos estabilidade nos proventos ao redor de R$ 0,10 a R$ 0,11 por cota, suportados pela taxa básica de juros que deve se manter elevada no médio prazo.",
            "reco_detalhe": "Excelente veículo para compor a parcela de renda do agronegócio com risco de crédito mitigado e isenção tributária. Peso recomendado de 4.5%."
        },
        {
            "ticker": "VISC11",
            "nome": "Vinci Shopping Centers FII",
            "segmento": "Shopping Centers (Tijolo)",
            "preco_atual": "R$ 110,00",
            "vpa": "R$ 117,00",
            "pvp": "0.94",
            "dy_12m": "9.5%",
            "ultimo_div": "R$ 0,85",
            "proj_preco": "Subir",
            "proj_div": "Subir",
            "reco": "Compra",
            "just_preco": "Desconto de 6% sobre o valor patrimonial. O fundo possui participações em shoppings de destaque nacional com portfólio muito bem diversificado geograficamente, o que reduz o risco regional e atrai fluxo consistente de investidores.",
            "just_div": "A melhora contínua da ocupação física (acima de 96%) e a diluição dos custos operacionais com a redução da inadimplência darão fôlego para que o rendimento mensal de R$ 0,85 cresça gradualmente para R$ 0,90.",
            "reco_detalhe": "Compra para diversificação comercial. O portfólio geográfico confere robustez e a gestão ativa da Vinci tem histórico sólido de geração de valor. Peso: 4.5%."
        },
        {
            "ticker": "TRXF11",
            "nome": "TRX Real Estate FII",
            "segmento": "Renda Urbana (Tijolo)",
            "preco_atual": "R$ 105,50",
            "vpa": "R$ 105,50",
            "pvp": "1.00",
            "dy_12m": "10.2%",
            "ultimo_div": "R$ 0,93",
            "proj_preco": "Subir",
            "proj_div": "Manter",
            "reco": "Compra",
            "just_preco": "O fundo foca em imóveis comerciais locados sob a modalidade 'built-to-suit' (construído sob medida) para grandes redes de varejo (Assaí, Pão de Açúcar, Leroy Merlin). A resiliência operacional desses inquilinos assegura a perenidade dos ativos.",
            "just_div": "A estrutura dos contratos atípicos reajustados pelo IPCA fornece um dividendo altamente estável e indexado. O rendimento atual de R$ 0,93 está garantido e com excelente visibilidade de fluxo de caixa futuro.",
            "reco_detalhe": "Recomendamos Compra para portfólios previdenciários de longo prazo devido à excelente proteção inflacionária contratual. Alocação: 6.0%."
        },
        {
            "ticker": "GGRC11",
            "nome": "GGR Copevi Renda FII",
            "segmento": "Logística / Industrial",
            "preco_atual": "R$ 11,20",
            "vpa": "R$ 12,44",
            "pvp": "0.90",
            "dy_12m": "11.0%",
            "ultimo_div": "R$ 0,10",
            "proj_preco": "Subir",
            "proj_div": "Manter",
            "reco": "Compra",
            "just_preco": "O fundo passou por um split de cotas (1:10) para melhorar a liquidez no secundário. Apresenta forte desconto patrimonial de 10%, operando com P/VP de 0.90, o que cria uma margem de segurança atrativa para investidores focados em tijolo logístico.",
            "just_div": "Os galpões industriais e logísticos estão majoritariamente sob contratos atípicos de longo prazo. A receita mensal é protegida e deve sustentar dividendos regulares de R$ 0,10 por cota (DY anual de ~11%), o que é muito alto para a classe de tijolos.",
            "reco_detalhe": "Recomendamos Compra pelo binômio atrativo de alto Dividend Yield em tijolo e forte desconto patrimonial. Alocação de 4.0% indicada."
        },
        {
            "ticker": "KNSC11",
            "nome": "Kinea Securities FII",
            "segmento": "Recebíveis (Papel)",
            "preco_atual": "R$ 88,20",
            "vpa": "R$ 92,84",
            "pvp": "0.95",
            "dy_12m": "11.8%",
            "ultimo_div": "R$ 0,85",
            "proj_preco": "Manter",
            "proj_div": "Manter",
            "reco": "Manutenção",
            "just_preco": "Fundo de papel de alta qualidade de crédito gerido pela Kinea. Negociado com leve desconto patrimonial de 5% (P/VP de 0.95). A estabilidade de preços das cotas é favorecida pela governança rigorosa da gestora.",
            "just_div": "A carteira é mista (IPCA e CDI), equilibrando o portfólio contra oscilações de juros e inflação. Os rendimentos mensais devem orbitar de forma constante entre R$ 0,82 e R$ 0,88, com perfil de baixo risco de crédito (high grade).",
            "reco_detalhe": "Excelente veículo para preservação de capital e rendimentos consistentes com volatilidade controlada. Alocação recomendada de 5.0%."
        },
        {
            "ticker": "XPLG11",
            "nome": "XP Log FII",
            "segmento": "Logística (Tijolo)",
            "preco_atual": "R$ 102,50",
            "vpa": "R$ 107,89",
            "pvp": "0.95",
            "dy_12m": "9.1%",
            "ultimo_div": "R$ 0,78",
            "proj_preco": "Subir",
            "proj_div": "Manter",
            "reco": "Compra",
            "just_preco": "O XP Log possui um portfólio robusto de galpões localizados nos principais eixos industriais do país. O desconto de 5% sobre o valor patrimonial representa uma excelente assimetria, já que o fundo tem vacância decrescente.",
            "just_div": "A receita operacional está consolidada, garantindo estabilidade no provento de R$ 0,78 por cota. Há gatilhos de reajustes contratuais e renovações imobiliárias que podem elevar ligeiramente a distribuição média no médio prazo.",
            "reco_detalhe": "Recomendamos Compra. Fundo de tijolo logístico de liquidez robusta e ativos qualificados. Ideal para compor o núcleo de tijolo. Alocação recomendada de 6.0%."
        },
        {
            "ticker": "IFRA11",
            "nome": "Itaú Active FI-Infra",
            "segmento": "FI-Infra (Infraestrutura)",
            "preco_atual": "R$ 97,71",
            "vpa": "R$ 95,80",
            "pvp": "1.02",
            "dy_12m": "13.5%",
            "ultimo_div": "R$ 1,10",
            "proj_preco": "Manter",
            "proj_div": "Manter",
            "reco": "Compra",
            "just_preco": "Fundo negociado com ágio condizente com a excelente qualidade do portfólio de crédito privado de infraestrutura (debêntures incentivadas de energia, saneamento e transportes). O prêmio de risco é altamente atrativo.",
            "just_div": "Por possuir ativos indexados ao IPCA + taxas elevadas (IPCA + 7.22% de yield médio), o fundo consegue distribuir rendimentos robustos mensais e isentos de IR para pessoa física, mantendo o poder de compra do investidor no longo prazo.",
            "reco_detalhe": "Ativos de infraestrutura têm forte proteção anticíclica e isenção fiscal, gerando dividend yield líquido imbatível. Peso sugerido de 5.0%."
        },
        {
            "ticker": "KNCA11",
            "nome": "Kinea Crédito Agro FIAGRO",
            "segmento": "FIAGRO (Crédito)",
            "preco_atual": "R$ 95,20",
            "vpa": "R$ 100,74",
            "pvp": "0.95",
            "dy_12m": "13.8%",
            "ultimo_div": "R$ 1,10",
            "proj_preco": "Manter",
            "proj_div": "Manter",
            "reco": "Compra",
            "just_preco": "O FIAGRO de crédito da Kinea negocia com desconto patrimonial atrativo de 5%. A Kinea é reconhecida como uma das melhores gestoras de crédito estruturado, o que confere forte proteção de crédito mesmo em anos mais difíceis para o produtor rural.",
            "just_div": "A carteira é indexada ao CDI, se beneficiando do cenário de Selic elevada no Brasil. Os proventos recorrentes de R$ 1,10 por cota representam um retorno líquido muito robusto e livre de impostos, bem sustentado pelas garantias reais dos CRAs.",
            "reco_detalhe": "Compra para exposição ao agronegócio de forma segura via crédito high grade. O desconto patrimonial atual cria excelente assimetria. Alocação: 5.0%."
        },
        {
            "ticker": "KNIP11",
            "nome": "Kinea Índices de Preços FII",
            "segmento": "Recebíveis (Papel)",
            "preco_atual": "R$ 93,21",
            "vpa": "R$ 93,93",
            "pvp": "0.99",
            "dy_12m": "10.4%",
            "ultimo_div": "R$ 0,85",
            "proj_preco": "Subir",
            "proj_div": "Subir",
            "reco": "Compra",
            "just_preco": "Fundo de CRI exclusivo para investidores qualificados que negocia com leve desconto patrimonial. O portfólio é de excelente qualidade (high grade), focado em inflação (IPCA + spread médio superior a 6.5%). Tendência de leve alta nas cotas corporativas.",
            "just_div": "Com a inflação brasileira IPCA projetada para patamares estáveis de 4.0% - 4.5% e o carregamento elevado da carteira, os proventos mensais devem apresentar crescimento gradual, recuperando o patamar de R$ 0,90 por cota nos próximos semestres.",
            "reco_detalhe": "Excelente veículo de proteção patrimonial contra surtos inflacionários e de altíssimo padrão de crédito. Alocação recomendada de 6.5%."
        },
        {
            "ticker": "KDIF11",
            "nome": "Kinea Infra FIC FIDC",
            "segmento": "FI-Infra (Infraestrutura)",
            "preco_atual": "R$ 125,00",
            "vpa": "R$ 120,24",
            "pvp": "1.04",
            "dy_12m": "14.0%",
            "ultimo_div": "R$ 1,45",
            "proj_preco": "Manter",
            "proj_div": "Manter",
            "reco": "Compra",
            "just_preco": "Fundo de debêntures de infraestrutura gerido pelo time de crédito da Kinea. Embora negocie com ágio de 4% pelo histórico imbatível de rentabilidade, o carrego de taxa real IPCA + 9.03% compensa com folga o ágio de mercado.",
            "just_div": "Os rendimentos distribuídos são isentos de imposto de renda para pessoa física e apresentam estabilidade exemplar. A distribuição mensal consistente de R$ 1,40 a R$ 1,50 deve prosseguir, suportada pelas tarifas de infraestrutura concessionária.",
            "reco_detalhe": "Compra para carteiras previdenciárias focadas em juros reais elevados e isenção tributária de longo prazo. Peso sugerido de 5.5%."
        }
    ]

    for index, asset in enumerate(assets_data):
        asset_flowables = []

        # 1. Header (Ticker & Name)
        header_data = [
            [
                Paragraph(f"<font color='#D4AF37'><b>{asset['ticker']}</b></font> &nbsp;&nbsp;|&nbsp;&nbsp; {asset['nome']}", 
                          ParagraphStyle('AssetTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=colors.HexColor('#FFFFFF')))
            ]
        ]
        header_table = Table(header_data, colWidths=[480])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0B2545')),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        asset_flowables.append(header_table)

        # 2. Indicators Sub-table
        ind_data = [
            [
                Paragraph("<b>Segmento</b>", cell_style_bold),
                Paragraph("<b>Cotação</b>", cell_style_bold),
                Paragraph("<b>VPA</b>", cell_style_bold),
                Paragraph("<b>P/VP</b>", cell_style_bold),
                Paragraph("<b>DY (12M)</b>", cell_style_bold),
                Paragraph("<b>Último Div.</b>", cell_style_bold),
            ],
            [
                Paragraph(asset['segmento'], cell_style_normal),
                Paragraph(asset['preco_atual'], cell_style_normal),
                Paragraph(asset['vpa'], cell_style_normal),
                Paragraph(asset['pvp'], cell_style_normal),
                Paragraph(asset['dy_12m'], cell_style_normal),
                Paragraph(asset['ultimo_div'], cell_style_normal),
            ]
        ]
        ind_table = Table(ind_data, colWidths=[100, 76, 76, 76, 76, 76])
        ind_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EEF4F8')),
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#F9F9FB')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D4AF37')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ]))
        asset_flowables.append(ind_table)

        # 3. Projections Table
        if asset['reco'] == 'Compra':
            reco_style_val = reco_compra
        elif asset['reco'] == 'Manutenção':
            reco_style_val = reco_manutencao
        else:
            reco_style_val = reco_venda

        proj_preco_styled = f"<font color='#2A7B4C'><b>{asset['proj_preco']}</b></font>" if asset['proj_preco'] == 'Subir' else (f"<font color='#D97706'><b>{asset['proj_preco']}</b></font>" if asset['proj_preco'] == 'Manter' else f"<font color='#C2410C'><b>{asset['proj_preco']}</b></font>")
        proj_div_styled = f"<font color='#2A7B4C'><b>{asset['proj_div']}</b></font>" if asset['proj_div'] == 'Subir' else (f"<font color='#D97706'><b>{asset['proj_div']}</b></font>" if asset['proj_div'] == 'Manter' else f"<font color='#C2410C'><b>{asset['proj_div']}</b></font>")

        proj_data = [
            [
                Paragraph("<b>Projeção Cotação:</b>", cell_style_bold),
                Paragraph(proj_preco_styled, reco_style_val),
                Paragraph("<b>Projeção Dividendo:</b>", cell_style_bold),
                Paragraph(proj_div_styled, reco_style_val),
            ]
        ]
        proj_table = Table(proj_data, colWidths=[110, 130, 110, 130])
        proj_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F4F7F6')),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#EEF4F8')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        asset_flowables.append(proj_table)

        # 4. Justifications
        just_text_p = Paragraph(f"<b>Tese Cotação:</b> {asset['just_preco']}<br/><b>Tese Dividendo:</b> {asset['just_div']}", body_justify)
        just_table = Table([[just_text_p]], colWidths=[480])
        just_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#EEF4F8')),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        asset_flowables.append(just_table)

        # 5. Recommendation Bar
        reco_box_bg = '#E6F4EA' if asset['reco'] == 'Compra' else ('#FEF3C7' if asset['reco'] == 'Manutenção' else '#FCE8E6')
        reco_text_color = '#137333' if asset['reco'] == 'Compra' else ('#B06000' if asset['reco'] == 'Manutenção' else '#C5221F')
        reco_label = f"RECOMENDAÇÃO: {asset['reco'].upper()} | {asset['reco_detalhe']}"
        reco_p = Paragraph(f"<font color='{reco_text_color}'><b>{reco_label}</b></font>", ParagraphStyle('RecoBar', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=10))

        reco_table = Table([[reco_p]], colWidths=[480])
        reco_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(reco_box_bg)),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor(reco_text_color)),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        asset_flowables.append(reco_table)

        story.append(KeepTogether(asset_flowables))
        story.append(Spacer(1, 14))

        # Add a PageBreak after every 2 assets to maintain strict page budget (2 per page)
        if index % 2 == 1:
            story.append(PageBreak())

    # ================= PAGE 12: PORTFOLIO ALLOCATION =================
    story.append(Paragraph("RELAÇÃO DE PORTFÓLIO MODELO E ALOCAÇÃO RECOMENDADA", h1_style))
    story.append(Spacer(1, 10))

    portfolio_desc = (
        "Com o objetivo de maximizar o retorno sob uma premissa de diversificação prudente, desenhamos a "
        "<b>Carteira de Investimentos Modelo FII 2026</b>. Esta carteira foi calibrada de forma balanceada, "
        "focando em ativos high grade resilientes de tijolo, com carregamento protegido de inflação em CRIs de "
        "excelente crédito (Kinea/XP), além de exposição estratégica à isenção tributária de FI-Infra e FIAGROs."
    )
    story.append(Paragraph(portfolio_desc, body_style))
    story.append(Spacer(1, 10))

    # Portfolio Table Headers
    port_headers = [
        Paragraph("<b>Ticker</b>", cell_style_bold),
        Paragraph("<b>Nome do Ativo</b>", cell_style_bold),
        Paragraph("<b>Segmento</b>", cell_style_bold),
        Paragraph("<b>Recomendação</b>", cell_style_bold),
        Paragraph("<b>Peso (%)</b>", cell_style_bold)
    ]

    port_table_data = [port_headers]

    # Portfolio Assets sorting by weight descending
    portfolio_weights = [
        ("HGLG11", "CSHG Logística (Pátria Log)", "Logística (Tijolo)", "Compra", "8.0%"),
        ("KNRI11", "Kinea Renda Imobiliária", "Híbrido (Lajes/Logística)", "Compra", "7.5%"),
        ("XPML11", "XP Malls FII", "Shopping Centers (Tijolo)", "Compra", "7.5%"),
        ("HGRU11", "Pátria Renda Urbana FII", "Renda Urbana (Tijolo)", "Compra", "7.0%"),
        ("BRCO11", "Bresco Logística FII", "Logística (Tijolo)", "Compra", "6.5%"),
        ("KNIP11", "Kinea Índices de Preços FII", "Recebíveis (Papel)", "Compra", "6.5%"),
        ("TRXF11", "TRX Real Estate FII", "Renda Urbana (Tijolo)", "Compra", "6.0%"),
        ("XPLG11", "XP Log FII", "Logística (Tijolo)", "Compra", "6.0%"),
        ("MXRF11", "Maxi Renda FII", "Recebíveis (Papel)", "Manutenção", "6.0%"),
        ("KDIF11", "Kinea Infra FIC FIDC", "FI-Infra (Infraestrutura)", "Compra", "5.5%"),
        ("LVBI11", "VBI Logístico FII", "Logística (Tijolo)", "Compra", "5.5%"),
        ("KNSC11", "Kinea Securities FII", "Recebíveis (Papel)", "Manutenção", "5.0%"),
        ("KNCA11", "Kinea Crédito Agro FIAGRO", "FIAGRO (Crédito)", "Compra", "5.0%"),
        ("IFRA11", "Itaú Active FI-Infra", "FI-Infra (Infraestrutura)", "Compra", "5.0%"),
        ("VISC11", "Vinci Shopping Centers FII", "Shopping Centers (Tijolo)", "Compra", "4.5%"),
        ("SNAG11", "Suno Agro FIAGRO", "FIAGRO (Crédito)", "Manutenção", "4.5%"),
        ("GGRC11", "GGR Copevi Renda FII", "Logística / Industrial", "Compra", "4.0%"),
        ("TVRI11", "Tivio Renda Imobiliária FII", "Agências Bancárias (Tijolo)", "Venda", "0.0%"),
    ]

    for ticker, nome, seg, reco, peso in portfolio_weights:
        if reco == 'Compra':
            reco_text = f"<font color='#2A7B4C'><b>{reco}</b></font>"
        elif reco == 'Manutenção':
            reco_text = f"<font color='#D97706'><b>{reco}</b></font>"
        else:
            reco_text = f"<font color='#C2410C'><b>{reco}</b></font>"

        row = [
            Paragraph(ticker, cell_style_normal),
            Paragraph(nome, cell_style_normal),
            Paragraph(seg, cell_style_normal),
            Paragraph(reco_text, cell_style_normal),
            Paragraph(f"<b>{peso}</b>", cell_style_normal)
        ]
        port_table_data.append(row)

    # Add Total Row
    port_table_data.append([
        Paragraph("<b>TOTAL CARTEIRA</b>", cell_style_bold),
        Paragraph("", cell_style_normal),
        Paragraph("", cell_style_normal),
        Paragraph("", cell_style_normal),
        Paragraph("<b>100.0%</b>", cell_style_bold)
    ])

    port_table = Table(port_table_data, colWidths=[65, 145, 120, 80, 70])
    port_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0B2545')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D4AF37')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#EEF4F8')),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.HexColor('#FFFFFF'), colors.HexColor('#F9F9FB')]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    
    # Set text color white for portfolio headers
    for i in range(5):
        port_table_data[0][i].style.textColor = colors.white

    story.append(port_table)
    story.append(Spacer(1, 15))

    disclaimer_text = (
        "<b>Aviso Legal (Disclaimer):</b> Este relatório é de natureza puramente informativa e foi elaborado para o "
        "uso exclusivo de investidores. As análises, projeções e opiniões aqui contidas são baseadas em dados "
        "públicos de mercado disponíveis em meados de 2026, não constituindo oferta de compra ou venda de valores mobiliários, "
        "tampouco promessa ou garantia de rentabilidade futura. Investimentos em renda variável estão sujeitos a "
        "oscilações do mercado e riscos de crédito inerentes aos devedores e imóveis investidos."
    )
    story.append(Paragraph(disclaimer_text, ParagraphStyle('Disclaimer', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7, leading=9.5, textColor=colors.HexColor('#555555'))))

    # Build the document using the NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Relatório PDF de Luxo gerado com sucesso!")


if __name__ == "__main__":
    build_pdf()