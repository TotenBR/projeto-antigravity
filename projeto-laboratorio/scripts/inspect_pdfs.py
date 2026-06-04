import os
from pypdf import PdfReader

pdf_dir = "/home/toten/projeto-antigravity/projeto-laboratorio/drive-download-20260603T200247Z-3-001 (2)"

def inspect_pdf(filename):
    filepath = os.path.join(pdf_dir, filename)
    print(f"--- Inspecionando: {filename} ---")
    try:
        reader = PdfReader(filepath)
        num_pages = len(reader.pages)
        print(f"Número de páginas: {num_pages}")
        
        # Tenta extrair texto das 2 primeiras páginas
        for i in range(min(2, num_pages)):
            text = reader.pages[i].extract_text()
            print(f"--- Página {i+1} (Primeiros 300 caracteres de texto extraído) ---")
            if text:
                print(text[:300])
            else:
                print("[Sem texto extraído nesta página]")
    except Exception as e:
        print(f"Erro ao ler PDF: {e}")
    print("\n")

if __name__ == "__main__":
    files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    for file in files:
        inspect_pdf(file)
