import os
import re
import json

WORKSPACE = "/home/toten/projeto-antigravity"
AGENT_DIR = os.path.join(WORKSPACE, ".agent")
VAULT_DIR = os.path.join(AGENT_DIR, "skills_vault")
CATALOG_PATH = os.path.join(AGENT_DIR, "skills_catalog.json")
DOWNLOADED_SKILLS_DIR = os.path.join(WORKSPACE, ".temp/downloaded_skills/skills")

def parse_front_matter(content):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}, content
    
    yaml_text = match.group(1)
    meta = {}
    in_tags = False
    
    for line in yaml_text.splitlines():
        line_strip = line.strip()
        if not line_strip:
            continue
            
        # Check if it is a tag list item
        if in_tags and (line.startswith("  - ") or line.startswith("- ")):
            tag = line_strip.lstrip("- ").strip("'\"")
            if "keywords" not in meta:
                meta["keywords"] = []
            meta["keywords"].append(tag)
            continue
            
        if ":" in line_strip:
            parts = line_strip.split(":", 1)
            key = parts[0].strip()
            val = parts[1].strip().strip("'\"")
            
            if key == "tags":
                in_tags = True
                meta["keywords"] = []
            else:
                in_tags = False
                meta[key] = val
                
    clean_content = content[match.end():]
    return meta, clean_content

def import_skills():
    if not os.path.exists(DOWNLOADED_SKILLS_DIR):
        print(f"Directory {DOWNLOADED_SKILLS_DIR} not found.")
        return
        
    os.makedirs(VAULT_DIR, exist_ok=True)
    
    existing_catalog = []
    existing_ids = set()
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            existing_catalog = json.load(f)
            existing_ids = {item["id"] for item in existing_catalog}
            
    print(f"Loaded {len(existing_catalog)} existing skills in catalog.")
    
    imported_count = 0
    
    # Iterate over the downloaded skills directory
    for item in sorted(os.listdir(DOWNLOADED_SKILLS_DIR)):
        item_path = os.path.join(DOWNLOADED_SKILLS_DIR, item)
        if not os.path.isdir(item_path):
            continue
            
        skill_file = os.path.join(item_path, "SKILL.md")
        if not os.path.exists(skill_file):
            continue
            
        try:
            with open(skill_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            meta, clean_content = parse_front_matter(content)
            
            skill_id = meta.get("name", item).strip()
            if skill_id in existing_ids:
                # Collision: skip
                continue
                
            description = meta.get("description", f"Skill for {skill_id}").strip()
            keywords = meta.get("keywords", [])
            if not keywords:
                keywords = [skill_id]
                
            # Add split terms of skill ID to keywords
            dir_words = skill_id.split("-")
            for w in dir_words:
                if len(w) > 2 and w not in keywords:
                    keywords.append(w)
                    
            vault_skill_dir = os.path.join(VAULT_DIR, skill_id, "agent")
            os.makedirs(vault_skill_dir, exist_ok=True)
            
            vault_skill_file = os.path.join(vault_skill_dir, "skill.md")
            with open(vault_skill_file, "w", encoding="utf-8") as f:
                f.write(content)
                
            existing_catalog.append({
                "id": skill_id,
                "name": skill_id.replace("-", " ").title(),
                "description": description,
                "keywords": keywords
            })
            existing_ids.add(skill_id)
            imported_count += 1
            
        except Exception as e:
            print(f"Error importing {item}: {e}")
            
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_catalog, f, indent=2, ensure_ascii=False)
        
    print(f"\nImport finished! Imported {imported_count} skills into the vault.")
    print(f"Total skills in catalog: {len(existing_catalog)}")

if __name__ == "__main__":
    import_skills()
