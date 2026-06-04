import os
import sys
import json
import shutil
import argparse

WORKSPACE = "/home/toten/projeto-antigravity"
AGENT_DIR = os.path.join(WORKSPACE, ".agent")
SKILLS_DIR = os.path.join(AGENT_DIR, "skills")
VAULT_DIR = os.path.join(AGENT_DIR, "skills_vault")
CATALOG_PATH = os.path.join(AGENT_DIR, "skills_catalog.json")

MCP_CATALOG_PATH = os.path.join(AGENT_DIR, "mcp_catalog.json")
ACTIVE_MCPS_PATH = os.path.join(AGENT_DIR, "active_mcps.json")

def setup_directories():
    os.makedirs(SKILLS_DIR, exist_ok=True)
    os.makedirs(VAULT_DIR, exist_ok=True)

def get_active_skills():
    if not os.path.exists(SKILLS_DIR):
        return set()
    active = set()
    for name in os.listdir(SKILLS_DIR):
        path = os.path.join(SKILLS_DIR, name)
        if os.path.isdir(path) or os.path.islink(path):
            active.add(name)
    return active

def get_active_mcps():
    if not os.path.exists(ACTIVE_MCPS_PATH):
        return ["filesystem", "fetch"] # Default baseline
    try:
        with open(ACTIVE_MCPS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return ["filesystem", "fetch"]

def write_active_mcps(mcp_ids):
    try:
        with open(ACTIVE_MCPS_PATH, "w", encoding="utf-8") as f:
            json.dump(list(mcp_ids), f, indent=2, ensure_ascii=False)
            print(f"Active MCPs saved: {', '.join(mcp_ids)}")
    except Exception as e:
        print(f"Error saving active MCPs: {e}")

def list_all():
    setup_directories()
    active_skills = get_active_skills()
    active_mcps = get_active_mcps()
    
    # List Skills
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        print("\n=== SKILLS CATALOGUE ===")
        for item in catalog:
            status = "🟢 ATIVA" if item["id"] in active_skills else "⚪ INATIVA"
            print(f"ID: {item['id']} | Status: {status}")
            print(f"Nome: {item['name']}")
            print(f"Descrição: {item['description']}")
            print("-" * 40)
            
    # List MCPs
    if os.path.exists(MCP_CATALOG_PATH):
        with open(MCP_CATALOG_PATH, "r", encoding="utf-8") as f:
            mcp_catalog = json.load(f)
        print("\n=== MCP SERVERS CATALOGUE ===")
        for item in mcp_catalog:
            status = "🟢 ATIVO (ONLINE)" if item["id"] in active_mcps else "⚪ INATIVO (OFFLINE)"
            print(f"ID: {item['id']} | Status: {status}")
            print(f"Nome: {item['name']}")
            print(f"Descrição: {item['description']}")
            print("-" * 40)

def activate_skill(skill_id):
    setup_directories()
    vault_path = os.path.join(VAULT_DIR, skill_id)
    active_path = os.path.join(SKILLS_DIR, skill_id)
    
    if not os.path.exists(vault_path):
        print(f"Erro: Skill '{skill_id}' não existe no vault.")
        return False
        
    if os.path.exists(active_path) or os.path.islink(active_path):
        print(f"Skill '{skill_id}' já está ativa.")
        return True
        
    try:
        os.symlink(vault_path, active_path)
        print(f"Skill ativada com sucesso: '{skill_id}'")
        return True
    except Exception as e:
        print(f"Erro ao criar link simbólico para '{skill_id}': {e}")
        return False

def deactivate_skill(skill_id):
    setup_directories()
    active_path = os.path.join(SKILLS_DIR, skill_id)
    
    if not (os.path.exists(active_path) or os.path.islink(active_path)):
        return True
        
    try:
        if os.path.islink(active_path):
            os.unlink(active_path)
        else:
            shutil.rmtree(active_path)
        print(f"Skill desativada com sucesso: '{skill_id}'")
        return True
    except Exception as e:
        print(f"Erro ao desativar skill '{skill_id}': {e}")
        return False

def auto_tune(query):
    setup_directories()
    query_words = set(query.lower().replace(",", " ").replace(".", " ").replace(";", " ").split())
    
    # 1. AUTO-TUNE SKILLS
    skills_activated = []
    skills_deactivated = []
    
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            catalog = json.load(f)
            
        for item in catalog:
            skill_id = item["id"]
            score = 0
            for keyword in item["keywords"]:
                if keyword.lower() in query_words:
                    score += 3
            desc_words = set(item["description"].lower().replace(",", " ").replace(".", " ").split())
            score += len(query_words.intersection(desc_words))
            
            if score >= 3:
                if activate_skill(skill_id):
                    skills_activated.append(skill_id)
            else:
                if deactivate_skill(skill_id):
                    skills_deactivated.append(skill_id)
                    
    # 2. AUTO-TUNE MCPS
    mcps_activated = []
    # Base baseline MCPs that are ALWAYS active for agent fundamentals
    active_mcps = {"filesystem", "fetch"}
    
    if os.path.exists(MCP_CATALOG_PATH):
        with open(MCP_CATALOG_PATH, "r", encoding="utf-8") as f:
            mcp_catalog = json.load(f)
            
        for item in mcp_catalog:
            mcp_id = item["id"]
            if mcp_id in {"filesystem", "fetch"}:
                continue
                
            score = 0
            for keyword in item["keywords"]:
                if keyword.lower() in query_words:
                    score += 3
            desc_words = set(item["description"].lower().replace(",", " ").replace(".", " ").split())
            score += len(query_words.intersection(desc_words))
            
            if score >= 3:
                active_mcps.add(mcp_id)
                mcps_activated.append(mcp_id)
                
        write_active_mcps(active_mcps)
        
    print("\n=== AUTO-TUNE CONCLUÍDO ===")
    print(f"Prompt de Contexto: '{query}'")
    print(f"Skills Ativadas: {', '.join(skills_activated) if skills_activated else 'Nenhuma'}")
    print(f"MCPs Adicionais Ativados: {', '.join(mcps_activated) if mcps_activated else 'Nenhum'}")
    print(f"Todos MCPs Ativos atualmente: {', '.join(active_mcps)}")

def main():
    parser = argparse.ArgumentParser(description="Gerenciador de Habilidades & MCPs")
    subparsers = parser.add_subparsers(dest="command", help="Comando")
    
    subparsers.add_parser("list", help="Lista todas as skills e MCPs e seus status")
    
    act_parser = subparsers.add_parser("activate", help="Ativa uma skill ou MCP")
    act_parser.add_argument("type", choices=["skill", "mcp"], help="Tipo a ativar")
    act_parser.add_argument("ids", nargs="+", help="IDs a serem ativados")
    
    deact_parser = subparsers.add_parser("deactivate", help="Desativa uma skill ou MCP")
    deact_parser.add_argument("type", choices=["skill", "mcp"], help="Tipo a desativar")
    deact_parser.add_argument("ids", nargs="+", help="IDs a serem desativados")
    
    tune_parser = subparsers.add_parser("auto", help="Auto-tuning baseado no prompt de contexto do projeto")
    tune_parser.add_argument("query", help="Descrição do que você quer fazer")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_all()
    elif args.command == "activate":
        if args.type == "skill":
            for sid in args.ids:
                activate_skill(sid)
        elif args.type == "mcp":
            active = set(get_active_mcps())
            for mid in args.ids:
                active.add(mid)
            write_active_mcps(active)
    elif args.command == "deactivate":
        if args.type == "skill":
            for sid in args.ids:
                deactivate_skill(sid)
        elif args.type == "mcp":
            active = set(get_active_mcps())
            for mid in args.ids:
                if mid in active:
                    active.remove(mid)
            write_active_mcps(active)
    elif args.command == "auto":
        auto_tune(args.query)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
