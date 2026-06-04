import os
import urllib.request
import urllib.parse
import bs4
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

# Config
WORKSPACE = "/home/toten/projeto-antigravity"
LIST_FILE = os.path.join(WORKSPACE, "LISTA DE FIIS.txt")
TEMP_DIR = os.path.join(WORKSPACE, ".temp")

os.makedirs(TEMP_DIR, exist_ok=True)

def get_fii_list():
    if not os.path.exists(LIST_FILE):
        return []
    with open(LIST_FILE, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
    return [line for line in lines if line and not line.startswith('#')]

def search_yahoo(fii_name):
    queries = [
        f"{fii_name} relatorio gerencial pdf",
        f"{fii_name} relatorio mensal pdf"
    ]
    links = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    for query in queries:
        url = f"https://search.yahoo.com/search?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=8) as response:
                html = response.read()
            soup = bs4.BeautifulSoup(html, 'html.parser')
            for a in soup.find_all('a', href=True):
                href = a['href']
                if 'r.search.yahoo.com' in href and '/RU=' in href:
                    try:
                        parts = href.split('/RU=')
                        if len(parts) > 1:
                            target_encoded = parts[1].split('/RK=')[0]
                            target_url = urllib.parse.unquote(target_encoded)
                            if target_url not in links:
                                links.append(target_url)
                    except Exception:
                        pass
        except Exception as e:
            print(f"[{fii_name}] Error searching query '{query}': {e}")
    return links

def download_and_validate(url, fii_name, index):
    dest_path = os.path.join(TEMP_DIR, f"{fii_name}_{index}.pdf")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            content_type = response.headers.get('Content-Type', '')
            data = response.read()
            
            # Check if it starts with PDF magic bytes or ends in .pdf or content-type is pdf
            is_pdf = data.startswith(b'%PDF') or 'application/pdf' in content_type.lower() or url.lower().endswith('.pdf')
            
            if is_pdf and len(data) > 10000:
                with open(dest_path, 'wb') as f:
                    f.write(data)
                print(f"[{fii_name}] Success: Downloaded report {index} from {url} ({len(data)} bytes)")
                return True
    except Exception as e:
        # print(f"[{fii_name}] Failed to download from {url}: {e}")
        pass
    return False

def process_fii(fii_name):
    print(f"[{fii_name}] Starting search...")
    links = search_yahoo(fii_name)
    downloaded = 0
    checked_urls = set()
    
    for link in links:
        if downloaded >= 2:
            break
        if link in checked_urls:
            continue
        checked_urls.add(link)
        
        # Don't try to download from yahoo itself or generic search pages
        if any(domain in link for domain in ['yahoo.com', 'google.com', 'microsoft.com', 'facebook.com', 'twitter.com']):
            continue
            
        success = download_and_validate(link, fii_name, downloaded + 1)
        if success:
            downloaded += 1
            
    if downloaded < 2:
        print(f"[{fii_name}] Warning: Only downloaded {downloaded}/2 reports.")
    return fii_name, downloaded

def main():
    fiis = get_fii_list()
    print(f"Loaded {len(fiis)} funds: {', '.join(fiis)}")
    
    results = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_fii, fii): fii for fii in fiis}
        for future in as_completed(futures):
            fii = futures[future]
            try:
                fii_name, count = future.result()
                results[fii_name] = count
            except Exception as e:
                print(f"[{fii}] Error in process thread: {e}")
                results[fii] = 0
                
    print("\n=== DOWNLOAD CONCLUÍDO ===")
    for fii, count in results.items():
        print(f"{fii}: {count}/2 relatórios baixados.")
        
    # Open the folder to show downloaded files to user
    try:
        subprocess.run(['xdg-open', TEMP_DIR], check=True)
        print(f"Opened folder on desktop: {TEMP_DIR}")
    except Exception as e:
        print(f"Could not open folder on desktop: {e}")

if __name__ == '__main__':
    main()
