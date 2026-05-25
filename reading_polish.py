import json
import urllib.parse

print("📖 Initiating the FOOLPROOF Reading Polish...")

with open('career_database.json', 'r') as f:
    db = json.load(f)

readings_upgraded = 0
papers_protected = 0

for branch, skills in db.items():
    for skill, links in skills.items():
        reading_url = links.get("reading", "")
        safe_skill = urllib.parse.quote_plus(skill)
            
        # THE ULTIMATE SAFEGUARD: ONLY touch it if it's explicitly a Google Search!
        # If it's literally ANYTHING else (a PDF, a paper, a blog), we protect it.
        if "google.com/search" in reading_url or reading_url.strip() == "":
            
            # Upgrade Google Searches to direct trusted platforms
            if branch in ["computer science", "electronics engineering"]:
                db[branch][skill]["reading"] = f"https://www.geeksforgeeks.org/search/?q={safe_skill}"
            else:
                db[branch][skill]["reading"] = f"https://en.wikipedia.org/wiki/Special:Search?search={safe_skill}"
                
            readings_upgraded += 1
        else:
            # It is a real link! Leave it completely untouched.
            papers_protected += 1

with open('career_database.json', 'w') as f:
    json.dump(db, f, indent=4)

print("\n=========================================")
print("🎉 FOOLPROOF UPGRADE COMPLETE!")
print(f"➔ Upgraded {readings_upgraded} Google Searches to Wikipedia/GFG.")
print(f"➔ Safely PROTECTED {papers_protected} real links (Papers, PDFs, etc.).")
print("=========================================")