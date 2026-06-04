import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

def create_pdf_report():
    pdf_path = "/home/toten/projeto-antigravity/Relatorio_Executivo_Processo.pdf"
    
    # Setup document
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = HexColor("#1A365D")  # Deep Navy
    secondary_color = HexColor("#4A5568")  # Slate Gray
    accent_color = HexColor("#2B6CB0")  # Accent Blue
    text_color = HexColor("#2D3748")  # Charcoal
    bg_color = HexColor("#F7FAFC")  # Off-white
    
    # Modify default styles or add new ones
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceAfter=25
    )
    
    h1_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=primary_color,
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=text_color,
        spaceAfter=10
    )
    
    bold_body_style = ParagraphStyle(
        'BoldBodyTextCustom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=primary_color
    )
    
    meta_val_style = ParagraphStyle(
        'MetaValue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=text_color
    )
    
    table_text_style = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=text_color
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.white
    )

    story = []
    
    # ------------------ HEADER ------------------
    story.append(Paragraph("RELATÓRIO JURÍDICO EXECUTIVO", title_style))
    story.append(Paragraph("Acompanhamento Processual Consolidado · TJMG Segunda Instância", subtitle_style))
    
    # ------------------ METADATA TABLE ------------------
    meta_data = [
        [
            Paragraph("Número Único CNJ", meta_label_style),
            Paragraph("1261945-42.2026.8.13.0000", meta_val_style),
            Paragraph("Número Interno TJMG", meta_label_style),
            Paragraph("1.0000.26.126193-7/001", meta_val_style)
        ],
        [
            Paragraph("Classe Judicial", meta_label_style),
            Paragraph("Agravo de Instrumento-Cv", meta_val_style),
            Paragraph("Órgão Julgador", meta_label_style),
            Paragraph("9ª Câmara Cível (TJMG)", meta_val_style)
        ],
        [
            Paragraph("Relator Atual", meta_label_style),
            Paragraph("Des. Leonardo de Faria Beraldo", meta_val_style),
            Paragraph("Data de Distribuição", meta_label_style),
            Paragraph("23/03/2026", meta_val_style)
        ],
        [
            Paragraph("Parte Agravante", meta_label_style),
            Paragraph("Nivia Gonçalves Pereira e outros", meta_val_style),
            Paragraph("Parte Agravada", meta_label_style),
            Paragraph("Elma Bernardes de Souza", meta_val_style)
        ],
        [
            Paragraph("Processo de Origem", meta_label_style),
            Paragraph("0418206-63.2008.8.13.0071<br/>(Cumprimento de Sentença)", meta_val_style),
            Paragraph("Situação Atual", meta_label_style),
            Paragraph("ATIVO (Autos Conclusos)", meta_val_style)
        ]
    ]
    
    # Col widths: 120, 150, 120, 150 -> total 540 (fits letter width 612 - 80 margin)
    meta_table = Table(meta_data, colWidths=[110, 160, 110, 160])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BOX', (0,0), (-1,-1), 1, primary_color),
    ]))
    
    story.append(meta_table)
    story.append(Spacer(1, 20))
    
    # ------------------ SECTION 1: RESUMO ------------------
    story.append(Paragraph("1. Resumo da Situação Atual do Processo", h1_style))
    resumo_text = (
        "O processo em análise trata-se de um <b>Agravo de Instrumento Cível</b> em tramitação perante a "
        "<b>9ª Câmara Cível do Tribunal de Justiça de Minas Gerais (TJMG)</b>, interposto por Nivia Gonçalves Pereira e outros "
        "contra decisão proferida pelo juízo de primeira instância nos autos do Cumprimento de Sentença nº "
        "0418206-63.2008.8.13.0071 (Comarca de Boa Esperança/MG), no qual figura como exequente/agravada a Sra. "
        "<b>Elma Bernardes de Souza</b>.<br/><br/>"
        "O recurso deu entrada no Tribunal em 19/03/2026, sendo distribuído por prevenção ao Desembargador Leonardo de Faria Beraldo "
        "após despacho do Juiz de Direito Convocado Sidnei Ponce. Atualmente, o processo encontra-se em estado <b>ATIVO</b>, com "
        "a última movimentação registrada em 26/05/2026, data em que houve a juntada de petição eletrônica pelas partes, que foi "
        "imediatamente conclusa para apreciação do Desembargador Relator. O processo aguarda julgamento de mérito pelo colegiado."
    )
    story.append(Paragraph(resumo_text, body_style))
    story.append(Spacer(1, 10))
    
    # ------------------ SECTION 2: DECISÕES ------------------
    story.append(Paragraph("2. Histórico das Últimas Decisões", h1_style))
    
    decisoes_headers = [
        Paragraph("Data", table_header_style),
        Paragraph("Relator", table_header_style),
        Paragraph("Decisão Interlocutória / Despacho", table_header_style)
    ]
    
    decisao_1 = [
        Paragraph("<b>23/03/2026</b>", table_text_style),
        Paragraph("Des. Sidnei Ponce (JD)", table_text_style),
        Paragraph(
            "Determinação de redistribuição por prevenção regimental: <i>'... determino que o feito seja redistribuído, "
            "por prevenção, na forma regimental, com as cautelas de praxe...'</i>. Esta decisão deu origem à redistribuição "
            "ao Des. Leonardo de Faria Beraldo.",
            table_text_style
        )
    ]
    
    decisao_2 = [
        Paragraph("<b>30/03/2026</b>", table_text_style),
        Paragraph("Des. Leonardo de F. Beraldo", table_text_style),
        Paragraph(
            "<b>Recebimento do recurso sem efeito suspensivo.</b> Significa que o agravo foi admitido para processamento, "
            "mas a decisão da primeira instância (favorável a Elma Bernardes de Souza) continua produzindo seus efeitos "
            "plenos enquanto o recurso não for julgado definitivamente.",
            table_text_style
        )
    ]
    
    decisoes_table_data = [decisoes_headers, decisao_1, decisao_2]
    decisoes_table = Table(decisoes_table_data, colWidths=[80, 120, 340])
    decisoes_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_color]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
    ]))
    
    story.append(decisoes_table)
    story.append(Spacer(1, 15))
    
    # ------------------ SECTION 3: FONTES ------------------
    story.append(Paragraph("3. Fontes de Publicação e Intimações", h1_style))
    fontes_text = (
        "As decisões proferidas foram regularmente disponibilizadas e publicadas por meio do "
        "<b>Diário da Justiça Eletrônico Nacional (DJEN)</b>, garantindo a ampla publicidade e o início dos prazos processuais para as partes:<br/>"
        "• <b>Publicação de 23/03/2026:</b> Remessa enviada ao DJEN para ciência da decisão de redistribuição (ordem 184) "
        "para Elma Bernardes de Souza, Sebastião Martins Pereira e Nivia Gonçalves Pereira.<br/>"
        "• <b>Publicação de 30/03/2026:</b> Remessa enviada ao DJEN para ciência da decisão que negou efeito suspensivo ao recurso, "
        "intimando todas as partes envolvidas.<br/>"
        "• <b>Disponibilização de Acórdão/Despacho:</b> As íntegras estão acessíveis publicamente no portal do TJMG "
        "(<a href='https://www.tjmg.jus.br' color='#2B6CB0'>www.tjmg.jus.br</a>) através do sistema de andamento processual de 2ª Instância."
    )
    story.append(Paragraph(fontes_text, body_style))
    story.append(Spacer(1, 10))
    
    # ------------------ SECTION 4: PRÓXIMOS PASSOS ------------------
    story.append(Paragraph("4. Análise e Próximos Passos Prováveis", h1_style))
    passos_text = (
        "1. <b>Manifestação da Agravada (Contraminuta):</b> A parte agravada (Elma Bernardes de Souza) tem o direito de apresentar "
        "suas contrarrazões ao recurso (contraminuta) no prazo legal de 15 dias úteis a contar da intimação oficial.<br/>"
        "2. <b>Apreciação da Petição Recente:</b> A petição juntada pelas partes em 26/05/2026 está sob análise do Desembargador "
        "Relator. Espera-se uma decisão interlocutória breve ou despacho determinando providências cartoriais.<br/>"
        "3. <b>Julgamento do Mérito do Agravo:</b> Após a manifestação da agravada e a inclusão em pauta de julgamento, a 9ª Câmara "
        "Cível julgará o mérito do Agravo de Instrumento, decidindo se reforma ou mantém a decisão interlocutória de 1ª instância "
        "referente ao Cumprimento de Sentença."
    )
    story.append(Paragraph(passos_text, body_style))
    
    # Build PDF
    doc.build(story)
    print(f"Report generated at {pdf_path}")
    
    # Open PDF automatically on user request
    try:
        import subprocess
        subprocess.run(["xdg-open", pdf_path], check=True)
        print("Opened PDF automatically on user desktop.")
    except Exception as e:
        print(f"Could not open PDF: {e}")


if __name__ == "__main__":
    create_pdf_report()
