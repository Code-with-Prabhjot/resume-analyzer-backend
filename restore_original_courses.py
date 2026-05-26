import json
import os
import shutil
import glob
import re

try:
    from docx import Document
except ImportError:
    os.system('pip install python-docx')
    from docx import Document

DB_FILE = 'career_database.json'
BACKUP_FILE = 'career_database_SAFETY_BACKUP.json'

def clean_url(url):
    if not url:
        return url
    markdown_match = re.search(r'\[.*?\]\((.*?)\)', url)
    if markdown_match:
        return markdown_match.group(1).strip()
    return url.strip()

def restore_courses():
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: {DB_FILE} not found!")
        return
    
    shutil.copyfile(DB_FILE, BACKUP_FILE)

    with open(DB_FILE, 'r') as f:
        master_db = json.load(f)

    restored_count = 0

    # --- PROCESS YOUR FIXED COMPUTER SCIENCE JSON FILE ---
    if os.path.exists('cs_fixed.json'):
        print("📂 Found clean cs_fixed.json file. Processing CS branch...")
        try:
            with open('cs_fixed.json', 'r', encoding='utf-8') as f:
                raw_content = f.read()
            # Clean up the bracket concatenations between 50-skill sets
            cleaned_string = re.sub(r'\}\s*\{', '},\n{', raw_content)
            parsed_blocks = json.loads(f"[{cleaned_string}]")
            
            for block in parsed_blocks:
                for branch_key, skills in block.items():
                    branch_lower = branch_key.lower().strip()
                    mapped_branch = "computer science" if "computer" in branch_lower or branch_lower in ["cs", "cs engineering"] else branch_lower
                    
                    if mapped_branch in master_db:
                        for skill_name, links in skills.items():
                            skill_lower = skill_name.lower().strip()
                            if skill_lower in master_db[mapped_branch]:
                                original_course = links.get("course")
                                if original_course:
                                    master_db[mapped_branch][skill_lower]["course"] = clean_url(original_course)
                                    restored_count += 1
        except Exception as e:
            print(f"   ⚠️ Could not read cs_fixed.json: {e}")

    # --- PROCESS THE REMAINING WORD FILES FOR THE OTHER BRANCHES ---
    docx_files = glob.glob('*.docx')
    for docx_file in docx_files:
        file_name = os.path.basename(docx_file)
        # Skip the original broken cs file if it's still in the folder
        if "cs skills" in file_name.lower():
            continue
            
        try:
            doc = Document(docx_file)
            full_text = [para.text for para in doc.paragraphs if para.text.strip()]
            raw_json_string = '\n'.join(full_text)
            
            cleaned_string = re.sub(r'\}\s*\{', '},\n{', raw_json_string)
            parsed_blocks = json.loads(f"[{cleaned_string}]")
            
            for block in parsed_blocks:
                for branch_name, skills in block.items():
                    branch_lower = branch_name.lower().strip()
                    
                    if branch_lower in master_db:
                        for skill_name, links in skills.items():
                            skill_lower = skill_name.lower().strip()
                            if skill_lower in master_db[branch_lower]:
                                original_course = links.get("course")
                                if original_course:
                                    master_db[branch_lower][skill_lower]["course"] = clean_url(original_course)
                                    restored_count += 1
        except Exception as e:
            print(f"   ⚠️ Skipping {file_name} due to an evaluation error.")

    # Save everything back to master database
    with open(DB_FILE, 'w') as f:
        json.dump(master_db, f, indent=4)

    print(f"\n✅ SUCCESS: Final Total Restored: {restored_count} original premium course links!")

if __name__ == "__main__":
    restore_courses()