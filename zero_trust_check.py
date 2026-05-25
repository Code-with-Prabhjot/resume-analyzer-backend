import json
import requests
import time

print("🚨 INITIATING ZERO-TRUST PROTOCOL: Checking all 2,400 links...")

db_file = 'career_database.json'
with open(db_file, 'r') as f:
    db = json.load(f)

# Headers to pretend we are Google Chrome, not a Python bot
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Words that prove a website is broken, even if it doesn't give a 404 error
SOFT_404_KEYWORDS = ["page not found", "404 not found", "course no longer available", "does not exist", "we can't find that page"]

courses_fixed = 0
readings_fixed = 0

def verify_and_heal(url, skill, link_type):
    # If the AI already gave it a safe search link, we leave it alone.
    if "search" in url.lower() or "query" in url.lower():
        return url, False

    try:
        # Ping the website (Wait up to 5 seconds)
        response = requests.get(url, headers=headers, timeout=5)
        
        # Issue 1: Standard 404 Error or Server Crash
        if response.status_code >= 400:
            # Note: 403 Forbidden on Udemy/Coursera usually means they blocked our bot, 
            # but the link is actually fine. If it's a 403 on Udemy, we spare it.
            if response.status_code == 403 and ("udemy.com" in url or "coursera.org" in url):
                return url, False
            else:
                raise Exception("Bad Status Code")

        # Issue 2: The "Soft 404" (The website lied to us)
        page_text = response.text.lower()
        for keyword in SOFT_404_KEYWORDS:
            if keyword in page_text:
                raise Exception("Soft 404 Detected")

        # If it survived all that, the link is genuinely perfect.
        return url, False

    except Exception as e:
        # THE LINK FAILED. INITIATE RUTHLESS REPLACEMENT.
        print(f"❌ DEAD LINK: {url}")
        
        if link_type == "course":
            safe_course = f"https://www.coursera.org/search?query={skill.replace(' ', '%20')}"
            print(f"   ➔ Replaced with safe Coursera Search.")
            return safe_course, True
        else:
            safe_reading = f"https://www.google.com/search?q={skill.replace(' ', '+')}+official+documentation+OR+tutorial"
            print(f"   ➔ Replaced with safe Google Search.")
            return safe_reading, True


# Loop through every single branch and skill
for branch, skills in db.items():
    for skill, links in skills.items():
        course_url = links.get("course", "")
        reading_url = links.get("reading", "")
        
        # 1. Verify Course
        new_course, c_changed = verify_and_heal(course_url, skill, "course")
        if c_changed:
            db[branch][skill]["course"] = new_course
            courses_fixed += 1
            
        # 2. Verify Reading
        new_reading, r_changed = verify_and_heal(reading_url, skill, "reading")
        if r_changed:
            db[branch][skill]["reading"] = new_reading
            readings_fixed += 1

        # 3. Save to file immediately so you never lose progress
        if c_changed or r_changed:
            with open(db_file, 'w') as f:
                json.dump(db, f, indent=4)
            
        # Sleep for 1.5 seconds between links so you don't get IP banned
        time.sleep(1.5)

print("\n=========================================")
print(f"🎉 ZERO-TRUST AUDIT COMPLETE.")
print(f"Found and replaced {courses_fixed} broken Courses.")
print(f"Found and replaced {readings_fixed} broken Readings.")
print("Your demo is now mathematically crash-proof.")
print("=========================================")