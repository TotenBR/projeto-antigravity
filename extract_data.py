import os
import json
import pypdf

WORKSPACE = "/home/toten/projeto-antigravity"
TEMP_DIR = os.path.join(WORKSPACE, ".temp")
OUTPUT_JSON = os.path.join(TEMP_DIR, "extracted_text.json")

def extract_pdf_info(pdf_path):
    try:
        reader = pypdf.PdfReader(pdf_path)
        num_pages = len(reader.pages)
        
        # Keywords of interest
        keywords = [
            "vacância", "vacancia", "inadimplência", "inadimplencia", 
            "alavancagem", "risco", "alocação", "alocacao", 
            "dividendo", "rendimento", "resultado", "alerta", 
            "comentário", "gestor", "portfólio"
        ]
        
        # Always extract the first 3 pages
        pages_to_extract = set(range(min(3, num_pages)))
        
        # Scan other pages for keywords
        for i in range(num_pages):
            try:
                page_text = reader.pages[i].extract_text() or ""
                if any(kw in page_text.lower() for kw in keywords):
                    pages_to_extract.add(i)
            except Exception:
                pass
                
        pages_to_extract = sorted(list(pages_to_extract))
        extracted_sections = []
        
        for page_idx in pages_to_extract:
            try:
                page_text = reader.pages[page_idx].extract_text() or ""
                if page_text.strip():
                    extracted_sections.append(f"--- Página {page_idx + 1} ---\n{page_text.strip()}")
            except Exception:
                pass
                
        return "\n\n".join(extracted_sections)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

def main():
    if not os.path.exists(TEMP_DIR):
        print("Temp directory does not exist.")
        return
        
    pdf_files = [f for f in os.listdir(TEMP_DIR) if f.endswith('.pdf')]
    print(f"Found {len(pdf_files)} PDF files in temp directory.")
    
    extracted_data = {}
    for filename in sorted(pdf_files):
        # Filename format: {FII_NAME}_{INDEX}.pdf
        parts = filename.split('_')
        if len(parts) >= 2:
            fii_name = parts[0]
            pdf_path = os.path.join(TEMP_DIR, filename)
            print(f"Extracting text from {filename}...")
            text = extract_pdf_info(pdf_path)
            
            if text:
                if fii_name not in extracted_data:
                    extracted_data[fii_name] = []
                extracted_data[fii_name].append({
                    "filename": filename,
                    "content": text[:15000] # Limit to 15k characters per report to avoid blowing context
                })
                
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=2)
        
    print(f"\nExtracted data saved to {OUTPUT_JSON}")

if __name__ == '__main__':
    main()
