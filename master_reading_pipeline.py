import json
import urllib.parse
import requests
import time

print("🧠 Initiating Master Reading Pipeline: Fetching Real Research Papers...")

with open('career_database.json', 'r') as f:
    db = json.load(f)

papers_found = 0
fallbacks_used = 0

for branch, skills in db.items():
    for skill, links in skills.items():
        safe_skill = urllib.parse.quote_plus(skill)
        
        try:
            # 1. Ask the Semantic Scholar API for an Open-Access Paper
            # We ask for 1 result, and request the 'openAccessPdf' and 'url' fields
            api_url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={safe_skill}&limit=1&fields=openAccessPdf,url"
            response = requests.get(api_url, timeout=5)
            data = response.json()
            
            # 2. Check if we got a real, working PDF or Paper URL!
            if 'data' in data and len(data['data']) > 0:
                paper = data['data'][0]
                
                # If there's a direct free PDF, use it!
                if paper.get('openAccessPdf') and paper['openAccessPdf'].get('url'):
                    db[branch][skill]["reading"] = paper['openAccessPdf']['url']
                    print(f"📄 TIER 1 (PDF Found): {skill}")
                    papers_found += 1
                
                # Otherwise, use the official Journal URL
                elif paper.get('url'):
                    db[branch][skill]["reading"] = paper['url']
                    print(f"📘 TIER 1 (Journal Found): {skill}")
                    papers_found += 1
                    
                else:
                    raise Exception("No usable URL in paper data")
            else:
                raise Exception("No papers found")
                
        except Exception as e:
            # 3. TIER 3 FALLBACK: Wikipedia / GFG
            if branch in ["computer science", "electronics engineering", "information science"]:
                db[branch][skill]["reading"] = f"https://www.google.com/search?q=site%3Ageeksforgeeks.org+{safe_skill}"
            else:
                db[branch][skill]["reading"] = f"https://en.wikipedia.org/wiki/Special:Search?search={safe_skill}"
            
            print(f"🛡️ TIER 3 (Fallback): {skill}")
            fallbacks_used += 1

        # Save immediately to prevent data loss
        with open('career_database.json', 'w') as f:
            json.dump(db, f, indent=4)
            
        # VERY IMPORTANT: The API is free, so we MUST wait 1.5 seconds 
        # between checks so they don't block our IP address.
        time.sleep(1.5)

print("\n=========================================")
print("🎉 MASTER PIPELINE COMPLETE!")
print(f"➔ Successfully found {papers_found} direct Research Papers/PDFs.")
print(f"➔ Applied {fallbacks_used} safe Wikipedia/GFG fallbacks.")
print("Your database is now highly academic and 100% crash-proof.")
print("=========================================")