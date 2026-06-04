import os
import sys
import subprocess

WORKSPACE = "/home/toten/projeto-antigravity"
PYTHON_BIN = os.path.join(WORKSPACE, "venv", "bin", "python")

if not os.path.exists(PYTHON_BIN):
    # Se o executável do venv não estiver nessa pasta específica, usa o padrão do sistema
    PYTHON_BIN = sys.executable

def run_step(script_name, description):
    print(f"\n==================================================")
    print(f"🚀 INICIANDO: {description} ({script_name})")
    print(f"==================================================")
    
    script_path = os.path.join(WORKSPACE, script_name)
    if not os.path.exists(script_path):
        print(f"Erro: Script {script_name} não encontrado no workspace.")
        return False
        
    try:
        # Executa desvinculando saídas caso necessário, mas para console mantemos síncrono para o log aparecer
        result = subprocess.run([PYTHON_BIN, script_path], check=True, text=True)
        if result.returncode == 0:
            print(f"✅ CONCLUÍDO COM SUCESSO: {description}")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERRO ao executar {script_name}: {e}")
    return False

def main():
    print("✨ INICIANDO PIPELINE AUTOMÁTICO DE ATUALIZAÇÃO DO DASHBOARD DE FIIs ✨")
    
    # Passo 1: Busca e download de PDFs de relatórios gerenciais na B3 via Yahoo Search
    if not run_step("mapear_ri.py", "Busca e download de relatórios gerenciais em PDF"):
        print("\nAborting: Falha no download dos PDFs.")
        sys.exit(1)
        
    # Passo 2: Extração seletiva do conteúdo textual dos PDFs baseados em palavras-chave de risco
    if not run_step("extract_data.py", "Extração de texto relevante dos PDFs"):
        print("\nAborting: Falha ao extrair texto dos PDFs.")
        sys.exit(1)
        
    # Passo 3: Envio de dados, análise de IA CNPI-grade com Gemini e regravação do data.js
    if not run_step("analisar_com_gemini.py", "Análise de investimentos automatizada com IA Gemini"):
        print("\nAborting: Falha na análise com a API do Gemini.")
        sys.exit(1)
        
    print(f"\n==================================================")
    print("🏆 PIPELINE AUTOMATIZADO CONCLUÍDO COM SUCESSO! 🏆")
    print("O arquivo data.js foi atualizado com as novas teses de IA.")
    print("Para colocar as atualizações no ar na Vercel, execute os seguintes comandos:")
    print("  git add data.js")
    print("  git commit -m \"docs: atualizacao automatica de analises com Gemini\"")
    print("  git push origin main")
    print(f"==================================================")

if __name__ == '__main__':
    main()
