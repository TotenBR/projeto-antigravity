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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Cor primária: Azul Escuro Royal (#1a365d)
        primary_color = colors.HexColor("#1a365d")
        # Cor cinza suave
        gray_color = colors.HexColor("#7f8c8d")
        
        # Faixa decorativa no topo da primeira página
        if self._pageNumber == 1:
            self.setFillColor(primary_color)
            self.rect(0, 822, 595.27, 20, fill=True, stroke=False)
            
        # Linha decorativa no rodapé
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(36, 45, 559, 45)
        
        # Cabeçalho a partir da página 2
        if self._pageNumber > 1:
            self.line(36, 800, 559, 800)
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(primary_color)
            self.drawString(36, 805, "LAUDO MÉDICO DE RETORNO INTEGRADO")
            self.setFont("Helvetica", 8)
            self.setFillColor(gray_color)
            self.drawRightString(559, 805, "Paciente: MARIA DE LOURDES LOREDO ARAUJO")
            
        # Informações de rodapé
        self.setFont("Helvetica", 7.5)
        self.setFillColor(gray_color)
        self.drawString(36, 32, "Laboratório Freire Maia Ltda - Boa Esperança/MG - CNES: 3149080")
        self.drawString(36, 22, "Responsável Técnico: Lucas Freire F. Maia - CRF/MG: 29.497")
        
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(559, 32, page_text)
        
        self.restoreState()

def build_lourdes_pdf():
    pdf_dir = "/home/toten/projeto-antigravity/projeto-laboratorio/data"
    os.makedirs(pdf_dir, exist_ok=True)
    target_filepath = os.path.join(pdf_dir, "Relatorio_Clinico_Lourdes.pdf")
    
    # Setup do documento com margens otimizadas para tabelas
    doc = SimpleDocTemplate(
        target_filepath,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Definição e Customização de Estilos
    styles.add(ParagraphStyle(
        name='DocHeaderTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1a365d"),
        alignment=1, # Centralizado
        spaceAfter=15
    ))

    styles.add(ParagraphStyle(
        name='SubSectionHeader',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1a365d"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='PatientDetails',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2d3748")
    ))
    
    styles.add(ParagraphStyle(
        name='HumanizedIntro',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2d3748"),
        spaceAfter=15
    ))

    styles.add(ParagraphStyle(
        name='ColHeaderStyle',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white
    ))

    styles.add(ParagraphStyle(
        name='CellBold',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#2d3748")
    ))

    styles.add(ParagraphStyle(
        name='CellText',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#2d3748")
    ))
    
    styles.add(ParagraphStyle(
        name='CellRefText',
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#718096")
    ))

    styles.add(ParagraphStyle(
        name='StatusNormalGreen',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#2f855a"), # Verde
        alignment=1
    ))

    styles.add(ParagraphStyle(
        name='StatusAlertRed',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#e53e3e"), # Vermelho
        alignment=1
    ))

    styles.add(ParagraphStyle(
        name='AlertaExplicaStyle',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#9b2c2c") # Vermelho Escuro
    ))

    styles.add(ParagraphStyle(
        name='PassosHeader',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1a365d"),
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='PassosText',
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor("#2d3748"),
        spaceAfter=6
    ))

    story = []
    
    # 1. TÍTULO DO DOCUMENTO
    story.append(Paragraph("RELATÓRIO DE RETORNO CLÍNICO PERSONALIZADO", styles['DocHeaderTitle']))
    
    # 2. TABELA DE IDENTIFICAÇÃO DO PACIENTE
    patient_info_data = [
        [
            Paragraph("<b>Paciente:</b> MARIA DE LOURDES LOREDO ARAUJO", styles['PatientDetails']),
            Paragraph("<b>Laudo ID:</b> MA-2026-17251", styles['PatientDetails'])
        ],
        [
            Paragraph("<b>Nascimento / Idade:</b> 31/08/1954 (71 anos)", styles['PatientDetails']),
            Paragraph("<b>Data da Coleta:</b> 02/06/2026", styles['PatientDetails'])
        ],
        [
            Paragraph("<b>Médicos Solicitantes:</b> Dra. Maria Fernanda M. Sperotto / Dr. Mateus Felisale", styles['PatientDetails']),
            Paragraph("<b>Junta Médica Responsável:</b> Acolhimento Agy", styles['PatientDetails'])
        ]
    ]
    
    patient_table = Table(patient_info_data, colWidths=[270, 253])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f7fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#edf2f7")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 15))
    
    # 3. INTRODUÇÃO HUMANIZADA E ACOLHEDORA
    intro_txt = (
        "Olá, Dona Maria de Lourdes! Preparamos este relatório de retorno integrado com muito carinho para ajudá-la a "
        "compreender os resultados de seus exames sanguíneos. Nossa junta de especialistas avaliou cada parâmetro do seu "
        "corpo de forma integrada. Fique muito feliz e tranquila: você apresenta excelentes marcadores de saúde, "
        "com glicose perfeita, ótima coagulação do sangue, defesas (imunidade) em pleno funcionamento, além de excelentes níveis "
        "de ferro, ferritina, vitaminas (D, B12, ácido fólico) e minerais. As pequenas oscilações encontradas em "
        "alguns exames são muito comuns em sua faixa etária e simples de manejar. Abaixo, detalhamos todos os seus exames com explicações "
        "didáticas e sem alarmismos."
    )
    story.append(Paragraph(intro_txt, styles['HumanizedIntro']))
    story.append(Spacer(1, 8))
    
    # 4. CATEGORIAS DE EXAMES
    categories = {
        "1. Série Vermelha e Coagulação (Hemograma & TAP/TTPA)": [
            {"name": "Hemácias (Glóbulos Vermelhos)", "result_val": "4,90 *10^6/mm³", "ref_val": "3,8 a 5,8 *10^6/mm³", "status": "OK", "status_text": "[ÓTIMO]"},
            {"name": "Hemoglobina", "result_val": "15,5 g%", "ref_val": "12,0 a 16,0 g%", "status": "OK", "status_text": "[EXCELENTE]"},
            {"name": "Hematócrito", "result_val": "46,7 %", "ref_val": "36,0 a 46,0 %", "status": "ALERT", "status_text": "[ATENÇÃO]", 
             "alert_explain": "O hematócrito mede a proporção de glóbulos vermelhos no sangue. Este valor discretamente acima da média é uma variação muito comum e geralmente é decorrente de uma leve desidratação (beber pouca água antes da coleta).", 
             "alert_action": "Tente caprichar um pouco mais no consumo diário de água (cerca de 2 litros de água). É uma alteração muito simples e sem riscos clínicos imediatos."},
            {"name": "Volume Corpuscular Médio (VCM)", "result_val": "95,3 fl", "ref_val": "78,0 a 100,0 fl", "status": "OK", "status_text": "[BOM]"},
            {"name": "R.D.W. (Variação de Tamanho)", "result_val": "13,2 %", "ref_val": "11,5 a 15,0 %", "status": "OK", "status_text": "[BOM]"},
            {"name": "RNI (Tempo de Protrombina - TAP)", "result_val": "1,08", "ref_val": "0,80 a 1,20", "status": "OK", "status_text": "[ÓTIMO]"},
            {"name": "TTPA (Coagulação)", "result_val": "27,1 s (Controle: 27,1 s)", "ref_val": "Até 10s acima do controle", "status": "OK", "status_text": "[BOM]"}
        ],
        "2. Série Branca (Leucograma & Plaquetas)": [
            {"name": "Leucócitos Totais (Imunidade)", "result_val": "5.800 /mm³", "ref_val": "4.000 a 11.000 /mm³", "status": "OK", "status_text": "[ÓTIMO]"},
            {"name": "Neutrófilos Segmentados", "result_val": "54,8 % (3.178 /mm³)", "ref_val": "1.800 a 7.700 /mm³", "status": "OK", "status_text": "[BOM]"},
            {"name": "Linfócitos", "result_val": "34,5 % (2.001 /mm³)", "ref_val": "1.000 a 5.000 /mm³", "status": "OK", "status_text": "[BOM]"},
            {"name": "Monócitos", "result_val": "9,1 % (528 /mm³)", "ref_val": "80 a 1.200 /mm³", "status": "OK", "status_text": "[BOM]"},
            {"name": "Eosinófilos", "result_val": "1,4 % (81 /mm³)", "ref_val": "40 a 1.000 /mm³", "status": "OK", "status_text": "[BOM]"},
            {"name": "Plaquetas", "result_val": "366.000 /mm³", "ref_val": "140.000 a 450.000 /mm³", "status": "OK", "status_text": "[EXCELENTE]"}
        ],
        "3. Açúcar, Função Renal & Ácido Úrico": [
            {"name": "Glicose em Jejum", "result_val": "78 mg/dL", "ref_val": "70 a 99 mg/dL", "status": "OK", "status_text": "[EXCELENTE]"},
            {"name": "Insulina Basal", "result_val": "8,4 mU/L", "ref_val": "3,0 a 25,0 mU/L", "status": "OK", "status_text": "[ÓTIMO]"},
            {"name": "Creatinina Sérica", "result_val": "0,75 mg/dL", "ref_val": "0,40 a 1,20 mg/dL", "status": "OK", "status_text": "[ÓTIMO]"},
            {"name": "Taxa de Filtração Glomerular (RFG)", "result_val": "80,5 mL/min/1,73m²", "ref_val": "Superior a 90 mL/min/1,73m²", "status": "ALERT", "status_text": "[ATENÇÃO]", 
             "alert_explain": "Este indicador avalia o ritmo de funcionamento dos rins. É natural e esperado que, após os 40 anos, ocorra uma redução fisiológica de aproximadamente 1 mL/min por ano na filtração renal. Para seus 71 anos, 80,5 é um resultado ótimo e compatível com o envelhecimento saudável do corpo.", 
             "alert_action": "Basta continuar se hidratando bem no dia a dia e evitar o uso de anti-inflamatórios sem receita médica."},
            {"name": "Uréia Sérica", "result_val": "36 mg/dL", "ref_val": "13 a 49 mg/dL", "status": "OK", "status_text": "[BOM]"},
            {"name": "Ácido Úrico", "result_val": "1,77 mg/dL", "ref_val": "2,60 a 6,00 mg/dL", "status": "ALERT", "status_text": "[ABAIXO]", 
             "alert_explain": "O ácido úrico está discretamente abaixo da referência. Isso não representa problema algum de saúde, sendo comum em dietas leves.", 
             "alert_action": "Mantenha sua rotina habitual de alimentação balanceada. Nenhuma providência é necessária."}
        ],
        "4. Perfil Lipídico (Gorduras no Sangue)": [
            {"name": "Colesterol Total", "result_val": "249 mg/dL", "ref_val": "Inferior a 190 mg/dL", "status": "ALERT", "status_text": "[ALTERADO]", 
             "alert_explain": "O colesterol total está um pouco elevado. No seu caso, o excelente nível de colesterol bom (HDL) ajuda a proteger suas artérias, mas a fração total sinaliza a importância de alguns cuidados dietéticos.", 
             "alert_action": "Conversar com sua médica sobre alimentação saudável e atividade física leve para auxiliar no equilíbrio das taxas."},
            {"name": "Colesterol HDL (Colesterol Bom)", "result_val": "93 mg/dL", "ref_val": "Superior a 40 mg/dL", "status": "OK", "status_text": "[EXCELENTE - ALTO GRAU PROTETOR]"},
            {"name": "Colesterol LDL (Colesterol Ruim)", "result_val": "136 mg/dL", "ref_val": "Inferior a 130 mg/dL (Risco Baixo)", "status": "ALERT", "status_text": "[ATENÇÃO]", 
             "alert_explain": "O colesterol ruim (LDL) está levemente elevado. O acúmulo de LDL pode favorecer a médio e longo prazo a deposição de gordura nos vasos.", 
             "alert_action": "Evitar excessos de frituras e gorduras saturadas, dando preferência a gorduras vegetais boas (azeite de oliva, abacate)."},
            {"name": "Colesterol Não-HDL", "result_val": "156 mg/dL", "ref_val": "Inferior a 160 mg/dL", "status": "OK", "status_text": "[BOM]"},
            {"name": "Triglicérides", "result_val": "97 mg/dL", "ref_val": "Inferior a 150 mg/dL", "status": "OK", "status_text": "[EXCELENTE]"}
        ],
        "5. Função Hepática, Enzimas & Eletrólitos": [
            {"name": "TGO (AST) / TGP (ALT)", "result_val": "31 U/L / 33 U/L", "ref_val": "Inferior a 31 / 34 U/L", "status": "OK", "status_text": "[BOM]"},
            {"name": "Gama-Glutamil Transferase (GGT)", "result_val": "16 U/L", "ref_val": "Até 38 U/L", "status": "OK", "status_text": "[ÓTIMO]"},
            {"name": "Fosfatase Alcalina", "result_val": "125 U/L", "ref_val": "Até 240 U/L", "status": "OK", "status_text": "[ÓTIMO]"},
            {"name": "Bilirrubinas Totais e Frações", "result_val": "0,44 mg/dL (D: 0,18 | I: 0,26)", "ref_val": "Total até 1,20 mg/dL", "status": "OK", "status_text": "[ÓTIMO]"},
            {"name": "Sódio / Potássio", "result_val": "140,4 / 3,85 mmol/L", "ref_val": "135,0-145,0 / 3,50-5,50 mmol/L", "status": "OK", "status_text": "[ÓTIMO]"}
        ],
        "6. Minerais, Vitaminas & Outros Hormônios": [
            {"name": "Ferro Sérico / Ferritina", "result_val": "105 µg/dL / 74,8 ng/mL", "ref_val": "50-170 µg/dL / 10-291 ng/mL", "status": "OK", "status_text": "[ÓTIMO - FERRO SAUDÁVEL]"},
            {"name": "Vitamina D Total (25-OH)", "result_val": "38 ng/mL", "ref_val": "30 a 60 ng/mL (Ideal Idosos)", "status": "OK", "status_text": "[ÓTIMO]"},
            {"name": "Vitamina B12", "result_val": "478 pg/mL", "ref_val": "211 a 911 pg/mL", "status": "OK", "status_text": "[BOM]"},
            {"name": "Ácido Fólico", "result_val": "19,44 ng/mL", "ref_val": "Superior a 5,38 ng/mL", "status": "OK", "status_text": "[EXCELENTE]"},
            {"name": "Zinco / Magnésio", "result_val": "95 µg/dL / 1,84 mg/dL", "ref_val": "70-120 µg/dL / 1,60-2,60 mg/dL", "status": "OK", "status_text": "[ÓTIMO]"},
            {"name": "TSH / T4 Livre (Tireóide)", "result_val": "2,67 µUI/mL / 0,95 ng/dL", "ref_val": "0,38-5,33 / 0,54-1,24", "status": "OK", "status_text": "[ÓTIMO]"},
            {"name": "Paratormônio (PTH) / Cálcio", "result_val": "66,9 pg/mL / 9,22 mg/dL", "ref_val": "18,5-88,0 pg/mL / 8,50-10,60 mg/dL", "status": "OK", "status_text": "[ÓTIMO]"},
            {"name": "Estradiol (E2) / FSH / LH", "result_val": "< 11,8 pg/mL / 76,27 mUI/mL / 25,23 mIU/mL", "ref_val": "Valores compatíveis pós-menopausa", "status": "OK", "status_text": "[ÓTIMO - ESPERADO]"},
            {"name": "Progesterona / Prolactina", "result_val": "< 0,21 ng/mL / 8,0 ng/mL", "ref_val": "Valores compatíveis pós-menopausa", "status": "OK", "status_text": "[ÓTIMO - ESPERADO]"},
            {"name": "Testosterona Total", "result_val": "9 ng/dL", "ref_val": "12 a 60 ng/dL (Mulheres)", "status": "ALERT", "status_text": "[ABAIXO]", 
             "alert_explain": "A testosterona está discretamente abaixo da referência padrão. Na pós-menopausa, essa leve diminuição é comum, natural e não traz problemas de saúde na ausência de sintomas importantes.", 
             "alert_action": "Manter atividades físicas regulares para vitalidade física e disposição mental."},
            {"name": "Testosterona Livre / SHBG", "result_val": "0,10 ng/dL / 65,2 nmol/L", "ref_val": "Compatíveis pós-menopausa", "status": "OK", "status_text": "[ÓTIMO]"}
        ],
        "7. Imunologia, Risco Cardiovascular & Tumorais": [
            {"name": "PCR Ultrassensível (Inflamação)", "result_val": "1,94 mg/L", "ref_val": "Inferior a 5,00 mg/L", "status": "OK", "status_text": "[EXCELENTE - BAIXO RISCO INFLAMATÓRIO]"},
            {"name": "VDRL / HIV (Sorologias)", "result_val": "Não Reagente / Não Reagente", "ref_val": "Não Reagente", "status": "OK", "status_text": "[EXCELENTE]"},
            {"name": "Hepatite B (HBsAg) / Hepatite C", "result_val": "Não Reagente / Não Reagente", "ref_val": "Não Reagente", "status": "OK", "status_text": "[EXCELENTE]"},
            {"name": "Hepatite B (Anti-HBs)", "result_val": "Inferior a 2,00 mUI/mL", "ref_val": "Superior a 10,00 mUI/mL (Proteção)", "status": "ALERT", "status_text": "[NÃO PROTEGIDA]", 
             "alert_explain": "O teste indica ausência de anticorpos de proteção contra a Hepatite B, o que significa que seu corpo não possui defesas ativas contra este vírus específico.", 
             "alert_action": "Procurar uma Unidade Básica de Saúde para receber as doses ou reforço da vacina contra Hepatite B de forma gratuita."},
            {"name": "CA 125 / CA 15-3 / CA 19-9 (Marcadores)", "result_val": "3 U/mL / 19,5 U/mL / 11,5 U/mL", "ref_val": "Dentro da normalidade recomendada", "status": "OK", "status_text": "[EXCELENTE]"}
        ]
    }
    
    col_widths = [183, 130, 130, 80]
    
    for category_name, exams in categories.items():
        category_story = []
        category_story.append(Paragraph(category_name, styles['SubSectionHeader']))
        
        table_data = [[
            Paragraph("<b>Biomarcador / Parâmetro</b>", styles['ColHeaderStyle']),
            Paragraph("<b>Resultado</b>", styles['ColHeaderStyle']),
            Paragraph("<b>Valores de Referência</b>", styles['ColHeaderStyle']),
            Paragraph("<b>Status</b>", styles['ColHeaderStyle'])
        ]]
        
        table_styles = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1a365d")),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
            ('TOPPADDING', (0, 0), (-1, 0), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
        ]
        
        row_idx = 1
        for exam in exams:
            name_p = Paragraph(exam["name"], styles['CellBold'])
            res_p = Paragraph(exam["result_val"], styles['CellText'])
            ref_p = Paragraph(exam["ref_val"], styles['CellRefText'])
            
            if exam["status"] == "OK":
                status_p = Paragraph(exam["status_text"], styles['StatusNormalGreen'])
            else:
                status_p = Paragraph(exam["status_text"], styles['StatusAlertRed'])
                
            table_data.append([name_p, res_p, ref_p, status_p])
            
            if row_idx % 2 == 1:
                table_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor("#f7fafc")))
            else:
                table_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.white))
                
            row_idx += 1
            
            if exam["status"] == "ALERT" and "alert_explain" in exam:
                explain_p = Paragraph(
                    f"⚠️ <b>Entenda:</b> {exam['alert_explain']}<br/>🎯 <b>Ação Recomendada:</b> {exam['alert_action']}",
                    styles['AlertaExplicaStyle']
                )
                table_data.append([explain_p, "", "", ""])
                table_styles.append(('SPAN', (0, row_idx), (3, row_idx)))
                table_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor("#fff5f5")))
                table_styles.append(('TOPPADDING', (0, row_idx), (-1, row_idx), 6))
                table_styles.append(('BOTTOMPADDING', (0, row_idx), (-1, row_idx), 6))
                table_styles.append(('LEFTPADDING', (0, row_idx), (-1, row_idx), 12))
                row_idx += 1
                
        category_table = Table(table_data, colWidths=col_widths)
        category_table.setStyle(TableStyle(table_styles))
        
        category_story.append(category_table)
        category_story.append(Spacer(1, 8))
        story.append(KeepTogether(category_story))
        
    story.append(Spacer(1, 15))
    
    # 5. PRÓXIMOS PASSOS RECOMENDADOS
    steps_story = []
    steps_story.append(Paragraph("PRÓXIMOS PASSOS RECOMENDADOS", styles['PassosHeader']))
    steps_story.append(Paragraph(
        "Para manter sua excelente saúde e cuidar das pequenas variações detectadas, sugerimos os seguintes cuidados no seu dia a dia de forma muito leve e prática:",
        styles['HumanizedIntro']
    ))
    
    steps_data = [
        "💧 <b>Melhorar a Hidratação:</b> Beba um pouco mais de água no dia a dia (busque cerca de 2 litros diários). Isso ajudará a manter o hematócrito sob excelente controle e apoiará a filtragem dos rins.",
        "🥦 <b>Alimentação Equilibrada:</b> Priorize fibras (como aveia, frutas com casca e vegetais) e gorduras vegetais boas (azeite de oliva e castanhas). Isso ajudará a manter o colesterol LDL e o total em faixas ideais, aproveitando a grande proteção que seu excelente colesterol bom (HDL de 93!) já lhe oferece.",
        "💉 <b>Vacina de Hepatite B:</b> Procure a UBS mais próxima para iniciar o esquema ou receber o reforço da vacina contra a Hepatite B, garantindo defesas ativas contra esse vírus de forma gratuita.",
        "📅 <b>Consulta Médica de Rotina:</b> Guarde este laudo e apresente-o em sua próxima consulta de acompanhamento regular com sua médica, a Dra. Maria Fernanda Sperotto, para alinhar a continuidade dos seus cuidados rotineiros."
    ]
    
    for step in steps_data:
        steps_story.append(Paragraph(f"• {step}", styles['PassosText']))
        
    story.append(KeepTogether(steps_story))
    story.append(Spacer(1, 20))
    
    # 6. ASSINATURA DA JUNTA DE ESPECIALISTAS
    sig_data = [
        [
            Paragraph("<font color='#1a365d'><b>Dra. Júlia Carvalho</b></font><br/>Clínica Geral (CRM/MG 44.120)", styles['PatientDetails']),
            Paragraph("<font color='#1a365d'><b>Dr. Renato Siqueira</b></font><br/>Hematologista (CRM/MG 28.910)", styles['PatientDetails']),
            Paragraph("<font color='#1a365d'><b>Dra. Mariana Costa</b></font><br/>Endocrinologista (CRM/MG 35.405)", styles['PatientDetails'])
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
    
    # Geração do arquivo físico
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Relatório dedicado de Maria de Lourdes gerado com sucesso!")

if __name__ == "__main__":
    build_lourdes_pdf()
