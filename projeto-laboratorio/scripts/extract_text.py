import os
from pypdf import PdfReader

pdf_dir = "/home/toten/projeto-antigravity/projeto-laboratorio/drive-download-20260603T200247Z-3-001 (2)"
output_dir = "/home/toten/projeto-antigravity/projeto-laboratorio/data"

def extract_text_from_pdf(pdf_filename, txt_filename):
    pdf_path = os.path.join(pdf_dir, pdf_filename)
    txt_path = os.path.join(output_dir, txt_filename)
    print(f"Extraindo texto de {pdf_filename} para {txt_filename}...")
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
    except Exception as e:
        print(f"Erro ao processar {pdf_filename}: {e}")

if __name__ == "__main__":
    files = sorted([f for f in os.listdir(pdf_dir) if f.endswith(".pdf")])
    for idx, file in enumerate(files):
        extract_text_from_pdf(file, f"paciente_{idx+1}.txt")
