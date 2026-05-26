import json
import urllib.parse
import os

CLEAN_DB = 'career_database_CLEANED.json'
FINAL_DB = 'career_database_FINAL_PRODUCTION.json'

# SET THIS TO TRUE IF YOU WANT TO NUKE UDEMY LINKS AND REPLACE THEM WITH FREE COURSERA LINKS
PURGE_UDEMY = True 

def fill_gaps():
    print("🚀 Starting Phase 3: The Gap Filler...")
    
    if not os.path.exists(CLEAN_DB):
        print(f"❌ Error: {CLEAN_DB} not found! Did you run the sweeper?")
        return

    with open(CLEAN_DB, 'r') as f:
        database = json.load(f)

    filled_count = 0
    udemy_purged_count = 0

    core_branches = ["civil engineering", "mechanical engineering", "electrical engineering", "electronics engineering"]

    for branch_name, skills in database.items():
        for skill_name, data in skills.items():
            current_course = data.get("course", "")
            
            # Condition to trigger a replacement:
            # 1. The link is empty (nuked by the sweeper)
            # 2. OR the link is Udemy and we decided to purge paid courses
            needs_replacement = False
            
            if not current_course:
                needs_replacement = True
            elif PURGE_UDEMY and "udemy.com" in current_course.lower():
                needs_replacement = True
                udemy_purged_count += 1

            if needs_replacement:
                encoded_skill = urllib.parse.quote_plus(skill_name)
                
                if branch_name.lower() in core_branches:
                    # Direct NPTEL internal portal search
                    new_url = f"https://onlinecourses.nptel.ac.in/explorer/search?keyword={encoded_skill}"
                else:
                    # Direct Coursera search
                    new_url = f"https://www.coursera.org/search?query={encoded_skill}"
                
                data["course"] = new_url
                filled_count += 1

    # Save the final, production-ready database
    with open(FINAL_DB, 'w') as f:
        json.dump(database, f, indent=4)

    print("\n🏁 Database Finalization Complete!")
    print(f"✅ Empty slots filled: {filled_count - udemy_purged_count}")
    if PURGE_UDEMY:
        print(f"🔥 Paid Udemy links purged and replaced: {udemy_purged_count}")
    print(f"\n🏆 Your ultimate, production-ready database is saved as: {FINAL_DB}")
    print("You can now rename this to 'career_database.json' and deploy!")

if __name__ == "__main__":
    fill_gaps()