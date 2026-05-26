import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

DB_FILE = 'career_database.json'
CLEAN_DB_FILE = 'career_database_CLEANED.json'
REPORT_FILE = 'dead_links_report.json'

# Mimic a real browser so Udemy/Coursera don't instantly block our ping
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def check_link(skill_data):
    branch, skill, url = skill_data
    if not url:
        return branch, skill, url, "Empty"

    try:
        # We only need the headers to check status, so we use a 5-second timeout
        response = requests.get(url, headers=HEADERS, timeout=5, stream=True)
        if response.status_code == 200:
            return branch, skill, url, "Alive"
        else:
            return branch, skill, url, f"Dead (Status: {response.status_code})"
    except requests.RequestException as e:
        return branch, skill, url, f"Dead (Connection Error)"

def sweep_database():
    print("🧹 Starting Phase 2: The Zero-Trust Link Sweeper...")
    
    with open(DB_FILE, 'r') as f:
        database = json.load(f)

    # Gather all links to check
    links_to_check = []
    for branch, skills in database.items():
        for skill, data in skills.items():
            if "course" in data and data["course"]:
                links_to_check.append((branch, skill, data["course"]))

    print(f"🔍 Found {len(links_to_check)} course links to test. Launching 20 parallel threads...")

    dead_links = {}
    alive_count = 0
    dead_count = 0

    # Run checks in parallel for massive speed
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_link, data): data for data in links_to_check}
        
        for future in as_completed(futures):
            branch, skill, url, status = future.result()
            
            if status == "Alive":
                alive_count += 1
            elif "Dead" in status:
                dead_count += 1
                # Log it for the report
                if branch not in dead_links:
                    dead_links[branch] = {}
                dead_links[branch][skill] = {"url": url, "error": status}
                
                # Remove the dead link from the database
                database[branch][skill]["course"] = ""

    # Save the cleaned database
    with open(CLEAN_DB_FILE, 'w') as f:
        json.dump(database, f, indent=4)

    # Save the report
    if dead_links:
        with open(REPORT_FILE, 'w') as f:
            json.dump(dead_links, f, indent=4)

    print("\n🏁 Audit Complete!")
    print(f"✅ Alive Links: {alive_count}")
    print(f"💀 Dead Links Nuked: {dead_count}")
    print(f"\nYour clean database is saved as: {CLEAN_DB_FILE}")
    if dead_count > 0:
        print(f"A full report of the dead links is saved in: {REPORT_FILE}")

if __name__ == "__main__":
    sweep_database()