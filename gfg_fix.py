import json
import urllib.parse

print("🚑 Initiating the GeeksForGeeks Rescue Protocol...")

with open('career_database.json', 'r') as f:
    db = json.load(f)

gfg_fixed = 0

for branch, skills in db.items():
    for skill, links in skills.items():
        reading_url = links.get("reading", "")
        
        # Only target the broken GFG search links we generated earlier
        if "geeksforgeeks.org/search/?q=" in reading_url:
            safe_skill = urllib.parse.quote_plus(skill)
            
            # Replace with a hard-locked Google Site Search
            new_url = f"https://www.google.com/search?q=site%3Ageeksforgeeks.org+{safe_skill}"
            db[branch][skill]["reading"] = new_url
            
            gfg_fixed += 1

with open('career_database.json', 'w') as f:
    json.dump(db, f, indent=4)

print("\n=========================================")
print("🎉 GFG RESCUE COMPLETE!")
print(f"➔ Upgraded {gfg_fixed} broken GFG links to Bulletproof Google Site Searches.")
print("➔ All papers, Wikipedia links, and courses remain untouched.")
print("=========================================")