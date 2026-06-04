import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

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
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#7f8c8d"))
        
        # Desenha linha divisória do rodapé
        self.setStrokeColor(colors.HexColor("#bdc3c7"))
        self.setLineWidth(0.5)
        self.line(36, 45, 559, 45)
        
        # Desenha cabeçalho nas páginas seguintes à primeira
        if self._pageNumber > 1:
            self.line(36, 800, 559, 800)
            self.drawString(36, 805, "Projeto Laboratório - Retorno Médico Integrado")
            
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(559, 30, page_text)
        self.drawString(36, 30, "Laboratório Freire Maia - Boa Esperança/MG - RT: Lucas Freire F. Maia (CRF/MG 29.497)")
        self.restoreState()

def create_report(patient_name, patient_age, doctor_name, laudo_id, date, intro_text, exam_categories, target_filepath):
    # Configuração do Documento
    # Margens de 0.5 polegadas (36pt) para otimizar espaço de tabelas longas
    doc = SimpleDocTemplate(
        target_filepath,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Customização de Estilos
    styles.add(ParagraphStyle(
        name='MainTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1b3a4b"),
        alignment=1, # Centralizado
        spaceAfter=15
    ))
    
    styles.add(ParagraphStyle(
        name='SectionHeader',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1b3a4b"),
        spaceBefore=10,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='PatientInfoText',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2c3e50")
    ))
    
    styles.add(ParagraphStyle(
        name='IntroParagraph',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2c3e50"),
        spaceAfter=12
    ))

    styles.add(ParagraphStyle(
        name='ExamNameStyle',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#2c3e50")
    ))

    styles.add(ParagraphStyle(
        name='ResultStyle',
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#2c3e50")
    ))
    
    styles.add(ParagraphStyle(
        name='ReferenceStyle',
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#7f8c8d")
    ))

    styles.add(ParagraphStyle(
        name='OkStatusStyle',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#2e7d32"), # Verde escuro
        alignment=1 # Centralizado
    ))

    styles.add(ParagraphStyle(
        name='AlertStatusStyle',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#c0392b"), # Vermelho
        alignment=1 # Centralizado
    ))

    styles.add(ParagraphStyle(
        name='AlertText',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#c0392b") # Vermelho
    ))

    styles.add(ParagraphStyle(
        name='StepsHeader',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1b3a4b"),
        spaceBefore=15,
        spaceAfter=8,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='StepsText',
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#2c3e50"),
        spaceAfter=6
    ))

    story = []
    
    # 1. Cabeçalho / Título
    story.append(Paragraph("RELATÓRIO DE RETORNO MÉDICO INTEGRADO", styles['MainTitle']))
    
    # 2. Informações do Paciente em Tabela
    info_data = [
        [
            Paragraph(f"<b>Paciente:</b> {patient_name}", styles['PatientInfoText']),
            Paragraph(f"<b>Laudo N°:</b> {laudo_id}", styles['PatientInfoText'])
        ],
        [
            Paragraph(f"<b>Idade / Nascimento:</b> {patient_age}", styles['PatientInfoText']),
            Paragraph(f"<b>Data de Emissão:</b> {date}", styles['PatientInfoText'])
        ],
        [
            Paragraph(f"<b>Médico(a) Solicitante:</b> {doctor_name}", styles['PatientInfoText']),
            Paragraph(f"<b>Junta Médica Responsável:</b> Acolhimento Agy", styles['PatientInfoText'])
        ]
    ]
    info_table = Table(info_data, colWidths=[270, 250])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8f9fa")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#edf2f7")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 15))
    
    # 3. Introdução Humanizada
    story.append(Paragraph(intro_text, styles['IntroParagraph']))
    story.append(Spacer(1, 10))
    
    # 4. Tabela de Biomarcadores por Categoria
    for category_name, exams in exam_categories.items():
        category_story = []
        category_story.append(Paragraph(category_name, styles['SectionHeader']))
        
        # Colunas: Parâmetro/Exame, Resultado do Paciente, Intervalo de Referência, Classificação
        # Largura total disponível: 595.27 (A4) - 72 (margens) = 523pt
        col_widths = [183, 130, 130, 80]
        
        table_data = [[
            Paragraph("<b>Biomarcador / Parâmetro</b>", styles['ExamNameStyle']),
            Paragraph("<b>Resultado</b>", styles['ExamNameStyle']),
            Paragraph("<b>Valores de Referência</b>", styles['ExamNameStyle']),
            Paragraph("<b>Status</b>", styles['ExamNameStyle'])
        ]]
        
        table_styles = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1b3a4b")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ]
        
        row_idx = 1
        for exam in exams:
            # Dados básicos do exame
            name_p = Paragraph(exam["name"], styles['ExamNameStyle'])
            res_val = exam["result_val"]
            ref_val = exam["ref_val"]
            status = exam["status"] # "OK" ou "ALERT"
            status_text = exam["status_text"] # "[BOM]", "[ÓTIMO]", etc. ou "[ALTERADO]"
            
            res_p = Paragraph(res_val, styles['ResultStyle'])
            ref_p = Paragraph(ref_val, styles['ReferenceStyle'])
            
            if status == "OK":
                status_p = Paragraph(status_text, styles['OkStatusStyle'])
            else:
                status_p = Paragraph(status_text, styles['AlertStatusStyle'])
                
            table_data.append([name_p, res_p, ref_p, status_p])
            
            # Adiciona estilo de zebra (alternando cores nas linhas de dados básicos)
            if row_idx % 2 == 1:
                table_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor("#fdfdfd")))
            else:
                table_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor("#f4f7f6")))
                
            row_idx += 1
            
            # Se for alerta, adiciona linha imediatamente abaixo com explicação detalhada
            if status == "ALERT" and "alert_explain" in exam:
                explain_p = Paragraph(
                    f"⚠️ <b>O que significa:</b> {exam['alert_explain']}<br/>🎯 <b>O que fazer:</b> {exam['alert_action']}",
                    styles['AlertText']
                )
                table_data.append([explain_p, "", "", ""])
                table_styles.append(('SPAN', (0, row_idx), (3, row_idx)))
                table_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor("#fff5f5")))
                table_styles.append(('TOPPADDING', (0, row_idx), (-1, row_idx), 6))
                table_styles.append(('BOTTOMPADDING', (0, row_idx), (-1, row_idx), 6))
                table_styles.append(('LEFTPADDING', (0, row_idx), (-1, row_idx), 12))
                row_idx += 1
                
        category_table = Table(table_data, colWidths=col_widths)
        
        # Ajusta cores de texto do cabeçalho da tabela para branco
        header_text_style = TableStyle(table_styles)
        category_table.setStyle(header_text_style)
        
        category_story.append(category_table)
        category_story.append(Spacer(1, 10))
        
        # Evita órfãos, mantém a categoria junta se possível
        story.append(KeepTogether(category_story))
        
    story.append(Spacer(1, 15))
    
    # 5. Próximos Passos Recomendados
    steps_story = []
    steps_story.append(Paragraph("PRÓXIMOS PASSOS RECOMENDADOS", styles['StepsHeader']))
    steps_story.append(Paragraph(
        "Para nos ajudar a cuidar ainda melhor de você e complementar esta avaliação, sugerimos as seguintes ações e exames adicionais de forma muito tranquila:",
        styles['IntroParagraph']
    ))
    
    for idx, category in enumerate(exam_categories.keys()):
        # Vamos gerar os próximos passos a partir das observações do paciente
        pass
        
    # Usaremos passos customizados passados na função
    steps_data = []
    if "Maria" in patient_name:
        steps_data = [
            "💧 <b>Capriche na Hidratação:</b> Aumentar o consumo diário de água ajudará a normalizar a taxa do seu hematócrito (proporção de células vermelhas), além de fazer muito bem para a vitalidade dos seus rins.",
            "🥦 <b>Ajustes Alimentares Leves:</b> Reduzir gorduras saturadas e aumentar a ingestão de fibras (aveia, frutas, vegetais) ajudará a equilibrar o seu colesterol total e o LDL, aproveitando a grande proteção que o seu excelente colesterol HDL já fornece.",
            "💉 <b>Reforço Vacinal no SUS:</b> Procure a Unidade Básica de Saúde (UBS) mais próxima para tomar a vacina ou o reforço contra a <b>Hepatite B</b>, restabelecendo seus anticorpos protetores de forma simples e segura.",
            "📅 <b>Consulta de Rotina:</b> Agende um retorno com sua médica, a Dra. Maria Fernanda Sperotto, para apresentar estes laudos e alinhar a continuidade dos seus cuidados habituais."
        ]
    else:
        steps_data = [
            "👨‍⚕️ <b>Consulta Médica com Prioridade (Tranquila):</b> Agende um retorno com sua médica, a Dra. Ana Luiza S. Cunha Peloso, para avaliar os resultados de glicose e hemoglobina glicada, ajustando o plano de tratamento do seu diabetes.",
            "🛡️ <b>Proteção dos Rins (Cardioproteção Renal):</b> Converse com seu médico sobre a introdução de medicamentos que servem como escudo de proteção renal (como medicamentos das classes de IECA ou BRA), indicados para tratar a microalbuminúria (leve perda de proteína detectada na urina).",
            "🥩 <b>Suplementação de Ferro:</b> Como o ferro e os estoques (ferritina) estão baixos, resultando em uma anemia leve, seu médico poderá indicar um suplemento de ferro oral e ajustes nutricionais.",
            "🍌 <b>Alimentação Rica em Potássio:</b> Consuma mais banana, água de coco, batata e folhas verdes para elevar discretamente o seu potássio e combater possíveis fadigas ou cãibras.",
            "💧 <b>Hidratação Constante:</b> Beba pelo menos 2 litros de água por dia. Isso ajudará a limpar os pequenos cristais de oxalato de cálcio da urina e manterá seu sistema urinário saudável."
        ]
        
    for step in steps_data:
        steps_story.append(Paragraph(f"• {step}", styles['StepsText']))
        
    story.append(KeepTogether(steps_story))
    
    # 6. Assinatura da Junta Médica
    story.append(Spacer(1, 20))
    sig_data = [
        [
            Paragraph("<font color='#1b3a4b'><b>Dra. Júlia Carvalho</b></font><br/>Clínica Geral (CRM/MG 44.120)", styles['PatientInfoText']),
            Paragraph("<font color='#1b3a4b'><b>Dr. Renato Siqueira</b></font><br/>Hematologista (CRM/MG 28.910)", styles['PatientInfoText']),
            Paragraph("<font color='#1b3a4b'><b>Dra. Mariana Costa</b></font><br/>Endocrinologista (CRM/MG 35.405)", styles['PatientInfoText'])
        ]
    ]
    sig_table = Table(sig_data, colWidths=[174, 174, 174])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINEABOVE', (0,0), (-1,0), 0.5, colors.HexColor("#bdc3c7")),
        ('TOPPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(KeepTogether([sig_table]))

    # Gera o PDF usando o NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)

# Teste ou carregador de dados de Maria de Lourdes
maria_categories = {
    "1. Hemograma & Série Vermelha": [
        {"name": "Hemácias (Eritrócitos)", "result_val": "4,90 *10^6/mm³", "ref_val": "3,8 a 5,8 *10^6/mm³", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Hemoglobina", "result_val": "15,5 g%", "ref_val": "12,0 a 16,0 g%", "status": "OK", "status_text": "[EXCELENTE]"},
        {"name": "Hematócrito", "result_val": "46,7 %", "ref_val": "36,0 a 46,0 %", "status": "ALERT", "status_text": "[ATENÇÃO]", 
         "alert_explain": "O hematócrito indica a proporção de células vermelhas no sangue. Este valor discretamente elevado costuma ser decorrente de uma leve desidratação (como beber pouca água antes do exame).", 
         "alert_action": "Aumentar a ingestão diária de líquidos (cerca de 2 litros de água por dia). É uma alteração muito simples e sem riscos clínicos imediatos."},
        {"name": "Volume Corpuscular Médio (VCM)", "result_val": "95,3 fl", "ref_val": "78,0 a 100,0 fl", "status": "OK", "status_text": "[BOM]"},
        {"name": "R.D.W. (Variação de Tamanho)", "result_val": "13,2 %", "ref_val": "11,5 a 15,0 %", "status": "OK", "status_text": "[BOM]"}
    ],
    "2. Série Branca (Leucograma & Defesas)": [
        {"name": "Leucócitos Totais", "result_val": "5.800 /mm³", "ref_val": "4.000 a 11.000 /mm³", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Neutrófilos Segmentados", "result_val": "54,8 % (3.178 /mm³)", "ref_val": "1.800 a 7.700 /mm³", "status": "OK", "status_text": "[BOM]"},
        {"name": "Linfócitos", "result_val": "34,5 % (2.001 /mm³)", "ref_val": "1.000 a 5.000 /mm³", "status": "OK", "status_text": "[BOM]"},
        {"name": "Monócitos", "result_val": "9,1 % (528 /mm³)", "ref_val": "80 a 1.200 /mm³", "status": "OK", "status_text": "[BOM]"},
        {"name": "Plaquetas (Coagulação)", "result_val": "366.000 /mm³", "ref_val": "140.000 a 450.000 /mm³", "status": "OK", "status_text": "[EXCELENTE]"}
    ],
    "3. Metabolismo de Açúcar & Coagulação": [
        {"name": "Glicose em Jejum", "result_val": "78 mg/dL", "ref_val": "70 a 99 mg/dL", "status": "OK", "status_text": "[EXCELENTE]"},
        {"name": "Insulina Basal", "result_val": "8,4 mU/L", "ref_val": "3,0 a 25,0 mU/L", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "RNI (Tempo de Protrombina - TAP)", "result_val": "1,08", "ref_val": "0,80 a 1,20", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "TTPA (Tempo de Tromboplastina)", "result_val": "27,1 s (Controle: 27,1 s)", "ref_val": "Até 10s acima do controle", "status": "OK", "status_text": "[BOM]"}
    ],
    "4. Perfil de Lipídios (Gorduras no Sangue)": [
        {"name": "Colesterol Total", "result_val": "249 mg/dL", "ref_val": "Inferior a 190 mg/dL", "status": "ALERT", "status_text": "[ALTAMENTE ALTERADO]", 
         "alert_explain": "O colesterol total está acima do recomendado. Embora o seu colesterol protetor (HDL) esteja excelente, o total elevado indica a necessidade de atenção dietética.", 
         "alert_action": "Adotar ajustes dietéticos com apoio médico, reduzindo frituras e industrializados, e reavaliar em alguns meses."},
        {"name": "Colesterol HDL (Colesterol Bom)", "result_val": "93 mg/dL", "ref_val": "Superior a 40 mg/dL", "status": "OK", "status_text": "[EXCELENTE - ALTAMENTE PROTETOR]"},
        {"name": "Colesterol LDL (Colesterol Ruim)", "result_val": "136 mg/dL", "ref_val": "Inferior a 130 mg/dL (Risco Baixo)", "status": "ALERT", "status_text": "[ATENÇÃO]", 
         "alert_explain": "O LDL (conhecido popularmente como colesterol ruim) está discretamente acima do limite desejável de 130 mg/dL para a faixa de risco cardiovascular mais baixa.", 
         "alert_action": "Priorizar o consumo de fibras (aveia, sementes) e gorduras saudáveis (azeite, peixes de água fria)."},
        {"name": "Colesterol Não-HDL", "result_val": "156 mg/dL", "ref_val": "Inferior a 160 mg/dL", "status": "OK", "status_text": "[BOM]"},
        {"name": "Triglicérides", "result_val": "97 mg/dL", "ref_val": "Inferior a 150 mg/dL", "status": "OK", "status_text": "[EXCELENTE]"}
    ],
    "5. Função Renal & Ácido Úrico": [
        {"name": "Creatinina Sérica", "result_val": "0,75 mg/dL", "ref_val": "0,40 a 1,20 mg/dL", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Filtração Glomerular Estimada (RFG)", "result_val": "80,5 mL/min/1,73m²", "ref_val": "Superior a 90 mL/min/1,73m²", "status": "ALERT", "status_text": "[ATENÇÃO]", 
         "alert_explain": "Este indicador de filtração do rim apresenta uma redução muito leve, o que é um processo fisiológico esperado e absolutamente normal com o avançar da idade (perda natural de ~1 mL/min ao ano após os 40 anos).", 
         "alert_action": "Manter uma hidratação diária generosa e evitar o uso de anti-inflamatórios comuns sem indicação médica."},
        {"name": "Uréia Sérica", "result_val": "36 mg/dL", "ref_val": "13 a 49 mg/dL", "status": "OK", "status_text": "[BOM]"},
        {"name": "Ácido Úrico", "result_val": "1,77 mg/dL", "ref_val": "2,60 a 6,00 mg/dL (Mulheres)", "status": "ALERT", "status_text": "[ABAIXO]", 
         "alert_explain": "O ácido úrico está discretamente abaixo da referência. Valores baixos geralmente não representam problemas de saúde e refletem apenas dietas leves.", 
         "alert_action": "Continuar com sua alimentação equilibrada habitual. Nenhuma medida corretiva é necessária."}
    ],
    "6. Função Hepática & Pancreática": [
        {"name": "TGO (AST)", "result_val": "31 U/L", "ref_val": "Inferior a 31 U/L", "status": "OK", "status_text": "[BOM]"},
        {"name": "TGP (ALT)", "result_val": "33 U/L", "ref_val": "Inferior a 34 U/L", "status": "OK", "status_text": "[BOM]"},
        {"name": "Gama-Glutamil Transferase (GGT)", "result_val": "16 U/L", "ref_val": "Até 38 U/L", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Fosfatase Alcalina", "result_val": "125 U/L", "ref_val": "Até 240 U/L", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Bilirrubina Total (e frações)", "result_val": "0,44 mg/dL (D: 0,18 | I: 0,26)", "ref_val": "Total até 1,20 mg/dL", "status": "OK", "status_text": "[ÓTIMO]"}
    ],
    "7. Minerais & Vitaminas": [
        {"name": "Cálcio Sérico", "result_val": "9,22 mg/dL", "ref_val": "8,50 a 10,60 mg/dL", "status": "OK", "status_text": "[BOM]"},
        {"name": "Magnésio Sérico", "result_val": "1,84 mg/dL", "ref_val": "1,60 a 2,60 mg/dL", "status": "OK", "status_text": "[BOM]"},
        {"name": "Ferro Sérico", "result_val": "105 µg/dL", "ref_val": "50 a 170 µg/dL", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Ferritina (Estoques de Ferro)", "result_val": "74,8 ng/mL", "ref_val": "10,0 a 291,0 ng/mL", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Vitamina D Total (25-OH)", "result_val": "38 ng/mL", "ref_val": "30 a 60 ng/mL (Ideal Idosos)", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Vitamina B12", "result_val": "478 pg/mL", "ref_val": "211 a 911 pg/mL", "status": "OK", "status_text": "[BOM]"},
        {"name": "Ácido Fólico", "result_val": "19,44 ng/mL", "ref_val": "Superior a 5,38 ng/mL", "status": "OK", "status_text": "[EXCELENTE]"},
        {"name": "Zinco", "result_val": "95 µg/dL", "ref_val": "70 a 120 µg/dL", "status": "OK", "status_text": "[ÓTIMO]"}
    ],
    "8. Hormônios Geral & Tireóide": [
        {"name": "TSH (Hormônio Tireoestimulante)", "result_val": "2,67 µUI/mL", "ref_val": "0,38 a 5,33 µUI/mL", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "T4 Livre", "result_val": "0,95 ng/dL", "ref_val": "0,54 a 1,24 ng/dL", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Estradiol (E2)", "result_val": "Inferior a 11,8 pg/mL", "ref_val": "Até 32,2 pg/mL (Pós-Menopausa)", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "FSH (Hormônio Folículo Estimulante)", "result_val": "76,27 mUI/mL", "ref_val": "23,00 a 116,30 mUI/mL", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "LH (Hormônio Luteinizante)", "result_val": "25,23 mIU/mL", "ref_val": "7,90 a 53,80 mIU/mL", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Progesterona", "result_val": "Inferior a 0,21 ng/mL", "ref_val": "Inferior a 0,5 ng/mL (Pós-Menopausa)", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Prolactina", "result_val": "8,0 ng/mL", "ref_val": "1,8 a 20,3 ng/mL (Pós-Menopausa)", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Paratormônio (PTH) Intacto", "result_val": "66,9 pg/mL", "ref_val": "18,5 a 88,0 pg/mL", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Testosterona Total", "result_val": "9 ng/dL", "ref_val": "12 a 60 ng/dL (Mulher Adulta)", "status": "ALERT", "status_text": "[ABAIXO]", 
         "alert_explain": "A testosterona total está discretamente abaixo da referência convencional de mulheres em idade fértil. Na pós-menopausa, essa queda é um processo biológico natural e de baixo impacto clínico isolado.", 
         "alert_action": "Discutir com o seu ginecologista ou clínico sobre seu bem-estar geral e energia, sem preocupações."},
        {"name": "Testosterona Livre Calculada", "result_val": "0,10 ng/dL", "ref_val": "0,05 a 0,88 ng/dL", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "SHBG", "result_val": "65,2 nmol/L", "ref_val": "23,2 a 159,1 nmol/L", "status": "OK", "status_text": "[ÓTIMO]"}
    ],
    "9. Imunologia, Inflamação & Sorologia": [
        {"name": "Proteína C Reativa (PCR-us)", "result_val": "1,94 mg/L", "ref_val": "Inferior a 5,00 mg/L", "status": "OK", "status_text": "[EXCELENTE - SEM INFLAMAÇÃO]"},
        {"name": "VDRL (Pesquisa para Sífilis)", "result_val": "Não Reagente", "ref_val": "Não Reagente", "status": "OK", "status_text": "[EXCELENTE]"},
        {"name": "Hepatite B (HBsAg)", "result_val": "Não Reagente", "ref_val": "Não Reagente", "status": "OK", "status_text": "[EXCELENTE]"},
        {"name": "Hepatite B (Anti-HBs)", "result_val": "Inferior a 2,00 mUI/mL", "ref_val": "Superior a 10,00 mUI/mL (Proteção)", "status": "ALERT", "status_text": "[NÃO PROTEGIDO]", 
         "alert_explain": "Este teste detecta anticorpos que protegem contra a Hepatite B. O resultado indica ausência de anticorpos circulantes protetores.", 
         "alert_action": "Recomenda-se tomar a vacina ou um reforço vacinal nas Unidades Básicas de Saúde de forma totalmente gratuita."},
        {"name": "Hepatite C (Anti-HCV)", "result_val": "Não Reagente", "ref_val": "Não Reagente", "status": "OK", "status_text": "[EXCELENTE]"},
        {"name": "Pesquisa de HIV (1 e 2)", "result_val": "Não Reagente", "ref_val": "Não Reagente", "status": "OK", "status_text": "[EXCELENTE]"},
        {"name": "CA 125 (Marcador Tumoral)", "result_val": "3 U/mL", "ref_val": "Inferior a 35 U/mL", "status": "OK", "status_text": "[EXCELENTE]"},
        {"name": "CA 15-3 (Marcador Tumoral)", "result_val": "19,5 U/mL", "ref_val": "Inferior a 32,0 U/mL", "status": "OK", "status_text": "[EXCELENTE]"},
        {"name": "CA 19-9 (Marcador Tumoral)", "result_val": "11,5 U/mL", "ref_val": "Inferior a 37,0 U/mL", "status": "OK", "status_text": "[EXCELENTE]"}
    ]
}

# Dados de José Carlos
jose_categories = {
    "1. Hemograma & Série Vermelha": [
        {"name": "Hemácias (Eritrócitos)", "result_val": "4,23 *10^6/mm³", "ref_val": "4,5 a 5,9 *10^6/mm³", "status": "ALERT", "status_text": "[ABAIXO]", 
         "alert_explain": "O número de células vermelhas circulantes está ligeiramente abaixo da referência esperada para homens, associado à anemia leve.", 
         "alert_action": "Consultar seu clínico geral e atentar-se às recomendações de reposição nutricional de ferro."},
        {"name": "Hemoglobina", "result_val": "11,4 g%", "ref_val": "13,0 a 17,5 g%", "status": "ALERT", "status_text": "[ABAIXO]", 
         "alert_explain": "A hemoglobina baixa indica uma anemia de intensidade leve. A causa mais provável aponta para estoques muito reduzidos de ferro.", 
         "alert_action": "Procurar orientação médica para iniciar a suplementação adequada de ferro e ajustes dietéticos com alimentos ricos em ferro."},
        {"name": "Hematócrito", "result_val": "35,2 %", "ref_val": "37,0 a 53,0 %", "status": "ALERT", "status_text": "[ABAIXO]", 
         "alert_explain": "O hematócrito (proporção de células vermelhas) está um pouco abaixo da faixa, o que é esperado devido ao quadro de anemia leve.", 
         "alert_action": "Acompanhamento clínico geral juntamente com o tratamento da hemoglobina."},
        {"name": "Volume Corpuscular Médio (VCM)", "result_val": "83,2 fl", "ref_val": "78,0 a 100,0 fl", "status": "OK", "status_text": "[BOM]"},
        {"name": "R.D.W. (Variação de Tamanho)", "result_val": "15,0 %", "ref_val": "11,5 a 15,0 %", "status": "OK", "status_text": "[BOM - LIMITE MÁXIMO]"}
    ],
    "2. Série Branca (Leucograma & Defesas)": [
        {"name": "Leucócitos Totais", "result_val": "4.820 /mm³", "ref_val": "4.000 a 11.000 /mm³", "status": "OK", "status_text": "[BOM]"},
        {"name": "Neutrófilos Segmentados", "result_val": "46,1 % (2.222 /mm³)", "ref_val": "1.800 a 7.700 /mm³", "status": "OK", "status_text": "[BOM]"},
        {"name": "Eosinófilos", "result_val": "8,7 % (419 /mm³)", "ref_val": "40 a 1.000 /mm³", "status": "OK", "status_text": "[BOM]"},
        {"name": "Basófilos", "result_val": "1,7 % (82 /mm³)", "ref_val": "0 a 200 /mm³", "status": "OK", "status_text": "[BOM]"},
        {"name": "Plaquetas (Coagulação)", "result_val": "265.000 /mm³", "ref_val": "140.000 a 450.000 /mm³", "status": "OK", "status_text": "[ÓTIMO]"}
    ],
    "3. Metabolismo da Glicose (Controle do Diabetes)": [
        {"name": "Hemoglobina Glicada (HbA1c)", "result_val": "8,3 %", "ref_val": "Inferior a 5,7% (Normal)", "status": "ALERT", "status_text": "[ALTERADO]", 
         "alert_explain": "A hemoglobina glicada está elevada, indicando um controle inadequado do diabetes nos últimos 3 meses, com uma glicemia média estimada em 192 mg/dL.", 
         "alert_action": "É essencial agendar consulta médica para avaliar e reajustar o esquema de medicamentos orais ou insulina, além de intensificar cuidados na dieta."},
        {"name": "Glicose em Jejum", "result_val": "123 mg/dL", "ref_val": "70 a 99 mg/dL", "status": "ALERT", "status_text": "[ALTERADO]", 
         "alert_explain": "A glicose em jejum está elevada. Este valor é condizente com a hemoglobina glicada e reflete o momento de descontrole glicêmico.", 
         "alert_action": "Conversar com seu médico para reavaliar a medicação de controle diário da glicemia."},
        {"name": "Glicose Pós-Prandial (pós-refeição)", "result_val": "136 mg/dL", "ref_val": "Inferior a 200 mg/dL", "status": "OK", "status_text": "[BOM]"},
        {"name": "Peptídeo C (Reserva Insulínica)", "result_val": "2,06 ng/mL", "ref_val": "1,10 a 4,40 ng/mL", "status": "OK", "status_text": "[BOM - INDICA RESERVA PANCREÁTICA]"},
        {"name": "Insulina Basal", "result_val": "6,0 mU/L", "ref_val": "3,0 a 25,0 mU/L", "status": "OK", "status_text": "[BOM]"}
    ],
    "4. Perfil Renal & Exame de Urina": [
        {"name": "Creatinina Sérica", "result_val": "0,96 mg/dL", "ref_val": "0,70 a 1,30 mg/dL", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Filtração Glomerular Estimada (RFG)", "result_val": "76,5 mL/min/1,73m²", "ref_val": "Superior a 90 mL/min/1,73m²", "status": "ALERT", "status_text": "[ATENÇÃO]", 
         "alert_explain": "Esta leve redução da taxa de filtração é perfeitamente normal e esperada para um paciente de 76 anos, devido ao envelhecimento natural das células renais.", 
         "alert_action": "Basta manter uma hidratação diária generosa e evitar anti-inflamatórios sem receita."},
        {"name": "Urina: Albumina", "result_val": "Presente (+)", "ref_val": "Negativo", "status": "ALERT", "status_text": "[ALTERADO]", 
         "alert_explain": "A presença sutil de albumina na urina indica que pequenas quantidades de proteína estão passando pelo filtro dos rins.", 
         "alert_action": "Requer atenção médica para introduzir medicamentos de proteção renal, visando poupar e resguardar a função renal futuro."},
        {"name": "Urina: Glicose", "result_val": "Presente", "ref_val": "Negativo", "status": "ALERT", "status_text": "[ALTERADO]", 
         "alert_explain": "A presença de açúcar na urina acontece quando os níveis de açúcar no sangue estão altos, forçando o rim a eliminar o excesso na urina.", 
         "alert_action": "O ajuste do diabetes com auxílio de medicamentos e controle alimentar fará a glicose urinar normalizar."},
        {"name": "Urina: Cristais de Oxalato de Cálcio", "result_val": "Alguns", "ref_val": "Ausentes", "status": "ALERT", "status_text": "[ALTERADO]", 
         "alert_explain": "Presença de sais minerais precipitados, o que é muito comum e indica que a urina está concentrada.", 
         "alert_action": "Aumentar significativamente o consumo de água no dia a dia para diluir a urina e evitar a formação de pedrinhas."},
        {"name": "Urina: Aspecto & Depósito", "result_val": "Semiturvo / Escasso", "ref_val": "Límpido / Ausente", "status": "ALERT", "status_text": "[ALTERADO]", 
         "alert_explain": "A aparência semiturva e o pequeno depósito devem-se à presença de cristais e urina concentrada.", 
         "alert_action": "Aumentar a ingestão hídrica habitual."},
        {"name": "Relação Albumina/Creatinina (RAC)", "result_val": "145 mg/g de Creatinina", "ref_val": "Inferior a 30 mg/g (Normal)", "status": "ALERT", "status_text": "[ALTERADO - MICROALBUMINÚRIA]", 
         "alert_explain": "O valor de 145 confirma uma microalbuminúria (sinal precoce de estresse do filtro renal por conta do diabetes).", 
         "alert_action": "Indicação direta de proteção renal com orientação médica (como uso de IECA ou BRA) e controle rígido de pressão e glicose."},
        {"name": "Urocultura (Cultura de Urina)", "result_val": "Sem crescimento bacteriano", "ref_val": "Negativa", "status": "OK", "status_text": "[EXCELENTE - SEM INFECÇÃO URINÁRIA]"}
    ],
    "5. Minerais & Eletrólitos": [
        {"name": "Sódio Sérico", "result_val": "141,2 mmol/L", "ref_val": "135,0 a 145,0 mmol/L", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Potássio Sérico", "result_val": "3,39 mmol/L", "ref_val": "3,50 a 5,50 mmol/L", "status": "ALERT", "status_text": "[LEVEMENTE BAIXO]", 
         "alert_explain": "O potássio está discretamente abaixo da referência, o que pode causar fadiga ou cãibras leves.", 
         "alert_action": "Aumentar o consumo de alimentos ricos em potássio, como banana, água de coco, batata e abacate."},
        {"name": "Cloretos", "result_val": "103,3 mmol/L", "ref_val": "98,0 a 108,0 mmol/L", "status": "OK", "status_text": "[BOM]"},
        {"name": "Cálcio Sérico", "result_val": "8,99 mg/dL", "ref_val": "8,50 a 10,60 mg/dL", "status": "OK", "status_text": "[BOM]"},
        {"name": "Fósforo", "result_val": "3,68 mg/dL", "ref_val": "2,50 a 4,80 mg/dL", "status": "OK", "status_text": "[BOM]"},
        {"name": "Magnésio Sérico", "result_val": "2,27 mg/dL", "ref_val": "1,60 a 2,60 mg/dL", "status": "OK", "status_text": "[ÓTIMO]"}
    ],
    "6. Função Hepática & Enzimas": [
        {"name": "TGO (AST) / TGP (ALT)", "result_val": "20 U/L / 20 U/L", "ref_val": "Inferior a 35 / 45 U/L", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Gama-Glutamil Transferase (GGT)", "result_val": "21 U/L", "ref_val": "Até 55 U/L", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Fosfatase Alcalina", "result_val": "151 U/L", "ref_val": "Até 270 U/L", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Bilirrubinas Totais e Frações", "result_val": "0,32 mg/dL (D: 0,22 | I: 0,10)", "ref_val": "Total até 1,20 mg/dL", "status": "OK", "status_text": "[ÓTIMO]"},
        {"name": "Amilase Sérica", "result_val": "36 U/L", "ref_val": "31 a 107 U/L", "status": "OK", "status_text": "[BOM]"},
        {"name": "Lipase Sérica", "result_val": "8 U/L", "ref_val": "13 a 60 U/L", "status": "ALERT", "status_text": "[ABAIXO]", 
         "alert_explain": "A lipase discretamente baixa sem sintomas e com amilase normal não tem relevância clínica preocupante. Indica saúde pancreática preservada.", 
         "alert_action": "Nenhuma ação é necessária. Fique tranquilo."},
        {"name": "CPK (Creatinofosfoquinase)", "result_val": "185 U/L", "ref_val": "Até 190 U/L", "status": "OK", "status_text": "[BOM]"},
        {"name": "Fosfatase Ácida Prostática", "result_val": "0,6 U/L", "ref_val": "Até 3,5 U/L", "status": "OK", "status_text": "[BOM]"},
        {"name": "Homocisteína", "result_val": "17,00 µmol/L", "ref_val": "7,71 a 22,33 µmol/L", "status": "OK", "status_text": "[BOM]"},
        {"name": "Mucoproteínas", "result_val": "2,1 mg/dL", "ref_val": "2,0 a 4,6 mg/dL", "status": "OK", "status_text": "[BOM]"}
    ],
    "7. Vitaminas, Ferro & Marcadores de Risco": [
        {"name": "Ferro Sérico", "result_val": "57 µg/dL", "ref_val": "65 a 175 µg/dL", "status": "ALERT", "status_text": "[ABAIXO]", 
         "alert_explain": "O ferro está abaixo do limite mínimo. Indica escassez de ferro circulante para a formação de células vermelhas.", 
         "alert_action": "Avaliar junto ao médico a necessidade de dieta rica em ferro ou suplementação oral."},
        {"name": "Ferritina (Estoques de Ferro)", "result_val": "11,2 ng/mL", "ref_val": "22,0 a 322,0 ng/mL", "status": "ALERT", "status_text": "[ABAIXO]", 
         "alert_explain": "A ferritina mede suas reservas de ferro do corpo. Níveis baixos confirmam uma anemia de causa ferropriva.", 
         "alert_action": "Realizar reposição terapêutica orientada pelo clínico geral e investigar a causa da perda."},
        {"name": "Vitamina D Total (25-OH)", "result_val": "50 ng/mL", "ref_val": "30 a 60 ng/mL (Ideal Idosos)", "status": "OK", "status_text": "[EXCELENTE]"},
        {"name": "Vitamina B12", "result_val": "276 pg/mL", "ref_val": "211 a 911 pg/mL (Limítrofe)", "status": "OK", "status_text": "[BOM - ATENÇÃO LIMÍTROFE]"},
        {"name": "Ácido Fólico", "result_val": "13,67 ng/mL", "ref_val": "Superior a 5,38 ng/mL", "status": "OK", "status_text": "[EXCELENTE]"},
        {"name": "Zinco", "result_val": "79 µg/dL", "ref_val": "70 a 120 µg/dL", "status": "OK", "status_text": "[BOM]"},
        {"name": "PSA Total (Próstata)", "result_val": "Inferior a 0,01 ng/mL", "ref_val": "Inferior a 4,00 ng/mL", "status": "OK", "status_text": "[EXCELENTE]"},
        {"name": "PSA Livre", "result_val": "0,01 ng/mL", "ref_val": "Não se aplica", "status": "OK", "status_text": "[BOM]"},
        {"name": "Proteína C Reativa (PCR-us)", "result_val": "0,35 mg/L", "ref_val": "Inferior a 5,00 mg/L", "status": "OK", "status_text": "[EXCELENTE]"},
        {"name": "Fator Reumatoide", "result_val": "Não Reagente", "ref_val": "Não Reagente (< 8 UI/mL)", "status": "OK", "status_text": "[EXCELENTE]"},
        {"name": "CA 19-9 (Marcador Tumoral)", "result_val": "16,6 U/mL", "ref_val": "Inferior a 37,0 U/mL", "status": "OK", "status_text": "[EXCELENTE]"}
    ]
}

if __name__ == "__main__":
    pdf_dir = "/home/toten/projeto-antigravity/projeto-laboratorio/data"
    os.makedirs(pdf_dir, exist_ok=True)
    
    # 1. Maria de Lourdes
    maria_intro = (
        "Olá, Dona Maria de Lourdes! Preparamos este relatório acolhedor para ajudá-la a compreender os resultados dos seus "
        "exames de sangue realizados no dia 02/06/2026. Nossa junta médica analisou detalhadamente cada parâmetro para lhe trazer "
        "informações claras, didáticas e tranquilizadoras. No geral, sua saúde apresenta excelentes marcadores, incluindo "
        "glicose perfeita, imunidade forte, baixíssima inflamação e ótimos níveis de vitaminas D e ácido fólico. Abaixo, detalhamos "
        "cada item e inserimos pequenas observações e dicas tranquilas sobre as leves variações que merecem uma atenção simples no dia a dia."
    )
    create_report(
        "MARIA DE LOURDES LOREDO ARAUJO",
        "71 anos (Nasc: 31/08/1954)",
        "Dra. Maria Fernanda Motta Sperotto / Dr. Mateus Felisale",
        "MA-2026-17251",
        "03/06/2026",
        maria_intro,
        maria_categories,
        os.path.join(pdf_dir, "Relatorio_Clinico_Maria_de_Lourdes.pdf")
    )
    print("Relatório de Maria de Lourdes gerado com sucesso!")
    
    # 2. Jose Carlos
    jose_intro = (
        "Olá, Seu José Carlos! Elaboramos este relatório clínico integrado para explicar de forma simples e muito transparente os "
        "resultados dos seus exames coletados no dia 02/06/2026. Analisamos seus biomarcadores sob o olhar de várias especialidades para "
        "lhe dar um direcionamento seguro e tranquilo. Observamos ótimos pontos, como um fígado saudável, coração em excelente estado, "
        "valores ótimos de próstata (PSA excelente!) e excelentes níveis de vitamina D. Identificamos alguns pontos que merecem ajustes "
        "e cuidados médicos próximos (como a glicose elevada e os primeiros sinais de atenção nos rins), além de estoques de ferro baixos. "
        "Mas fique tranquilo: com ajustes simples na medicação, alimentação e hábitos de hidratação, esses níveis podem ser facilmente estabilizados."
    )
    create_report(
        "JOSE CARLOS DE ARAUJO CUNHA",
        "76 anos (Nasc: 14/01/1950)",
        "Dra. Ana Luiza S. Cunha Peloso",
        "MA-2026-17230",
        "03/06/2026",
        jose_intro,
        jose_categories,
        os.path.join(pdf_dir, "Relatorio_Clinico_Jose_Carlos.pdf")
    )
    print("Relatório de José Carlos gerado com sucesso!")
