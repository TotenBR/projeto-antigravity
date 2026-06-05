import urllib.request
import re
import os
import time

def get_vpa(ticker):
    paths = ["fundos-imobiliarios", "fiagros", "fi-infra"]
    for path in paths:
        url = f"https://statusinvest.com.br/{path}/{ticker.lower()}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            html = urllib.request.urlopen(req).read().decode('utf-8')
            match = re.search(r'Val\. patrimonial p/cota.*?<strong class="value">([0-9,]+)</strong>', html, re.DOTALL | re.IGNORECASE)
            if match:
                val_str = match.group(1).replace(',', '.')
                return float(val_str)
        except urllib.error.HTTPError as e:
            # Se der 404, tenta o próximo path
            if e.code == 404:
                continue
            else:
                print(f"Erro HTTP {e.code} para {ticker} em {path}")
        except Exception as e:
            print(f"Erro ao buscar VPA para {ticker}: {e}")
    return None

def main():
    data_file = "/home/toten/projeto-antigravity/data.js"
    
    with open(data_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Encontrar todos os tickers no arquivo
    tickers = re.findall(r'"ticker":\s*"([A-Z0-9]{5,6})"', content)
    print(f"Encontrados {len(tickers)} FIIs para atualizar o VPA.")

    for ticker in tickers:
        print(f"Buscando VPA para {ticker}...", end=" ")
        vpa = get_vpa(ticker)
        if vpa is not None:
            print(f"R$ {vpa:.2f}")
            # Substituir o valor antigo no arquivo
            # Ex: "ticker": "XPML11", ... "vpa": 112.5,
            # Vamos usar uma regex que procura o ticker e altera o VPA dentro daquele bloco
            # Pattern para capturar do ticker até o vpa
            pattern = re.compile(rf'("ticker":\s*"{ticker}".*?"vpa":\s*)([0-9.]+)(,)', re.DOTALL)
            
            def repl(m):
                return f"{m.group(1)}{vpa}{m.group(3)}"
                
            content = pattern.sub(repl, content)
        else:
            print("Não encontrado!")
            
        time.sleep(1) # Pausa amigável para não sobrecarregar o StatusInvest

    with open(data_file, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Atualização concluída com sucesso! data.js salvo.")

if __name__ == "__main__":
    main()
