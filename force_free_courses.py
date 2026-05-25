import json
import urllib.parse

print("💸 Forcing 100% Free Courses...")

with open('career_database.json', 'r') as f:
    db = json.load(f)

courses_fixed = 0

for branch, skills in db.items():
    for skill, links in skills.items():
        # URL encode the skill (turns "machine learning" into "machine+learning")
        safe_skill = urllib.parse.quote_plus(skill)
        
        # Overwrite EVERY course with a search for Free certificates
        db[branch][skill]["course"] = f"https://www.classcentral.com/search?q={safe_skill}&free=true"
        courses_fixed += 1

with open('career_database.json', 'w') as f:
    json.dump(db, f, indent=4)

print(f"🎉 DONE! Successfully updated {courses_fixed} courses to guarantee 100% free options.")