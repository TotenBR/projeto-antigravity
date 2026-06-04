import os
import sys
import subprocess

WORKSPACE = "/home/toten/projeto-antigravity"
PYTHON_BIN = os.path.join(WORKSPACE, "venv", "bin", "python")

if not os.path.exists(PYTHON_BIN):
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
        result = subprocess.run([PYTHON_BIN, script_path], check=True, text=True)
        if result.returncode == 0:
            print(f"✅ CONCLUÍDO COM SUCESSO: {description}")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERRO ao executar {script_name}: {e}")
    return False

def run_git_upload():
    print(f"\n==================================================")
    print("📤 ENVIANDO ATUALIZAÇÕES PARA O GITHUB...")
    print("==================================================")
    try:
        # Adiciona o data.js modificado
        subprocess.run(["git", "add", "data.js"], check=True, cwd=WORKSPACE)
        
        # Faz o commit automático
        subprocess.run(["git", "commit", "-m", "docs: atualizacao automatica de analises com Gemini"], check=True, cwd=WORKSPACE)
        
        # Faz o push para a branch main
        subprocess.run(["git", "push", "origin", "main"], check=True, cwd=WORKSPACE)
        
        print("✅ Envio ao GitHub concluído! O deploy na Vercel foi iniciado automaticamente.")
        return True
    except subprocess.CalledProcessError as e:
        # Se não houver nada para commitar, o git commit retorna erro 1, tratamos isso
        print(f"⚠️ Aviso ou erro durante o envio ao Git: {e}")
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
        
    # Passo 4: Upload automático para o GitHub
    run_git_upload()
        
    print(f"\n==================================================")
    print("🏆 PIPELINE AUTOMATIZADO CONCLUÍDO COM SUCESSO! 🏆")
    print("O arquivo data.js foi atualizado e enviado para o GitHub.")
    print("O deploy automático do seu dashboard de FIIs está em andamento na Vercel.")
    print(f"==================================================")

if __name__ == '__main__':
    main()
