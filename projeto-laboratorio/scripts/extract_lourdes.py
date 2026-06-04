import os
from pypdf import PdfReader

pdf_path = "/home/toten/projeto-antigravity/projeto-laboratorio/drive-download-20260603T200247Z-3-001 (2)/lourdes.pdf"
txt_path = "/home/toten/projeto-antigravity/projeto-laboratorio/data/lourdes_texto.txt"

print(f"Extraindo texto de {pdf_path} para {txt_path}...")
try:
    reader = PdfReader(pdf_path)
    full_text = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            full_text.append(f"=== PÁGINA {i+1} ===\n{text}\n")
        else:
            full_text.append(f"=== PÁGINA {i+1} ===\n[Sem texto extraível nesta página]\n")
    
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(full_text))
    print(f"Extraído com sucesso! Total de páginas: {len(reader.pages)}")
    
    # Imprime as primeiras 5 linhas para checagem do paciente
    print("--- Primeiras linhas ---")
    with open(txt_path, "r", encoding="utf-8") as f:
        for _ in range(10):
            print(f.readline().strip())
except Exception as e:
    print(f"Erro ao processar: {e}")
