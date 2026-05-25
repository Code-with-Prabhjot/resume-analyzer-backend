import json

# Make sure this matches your current file name!
with open('career_database.json', 'r') as f:
    db = json.load(f)

print("🔍 Hunting for skipped YouTube links...")
missing_count = 0

for branch, skills in db.items():
    for skill, links in skills.items():
        yt_link = links.get("youtube", "")
        # If it still has "search_query", the big script missed it!
        if "search_query" in yt_link:
            print(f"⚠️ Missed Skill: '{skill}' (in {branch})")
            missing_count += 1

print(f"\nTotal missed: {missing_count}")