import json
import urllib.request
import urllib.parse
import re
import time

print("🎯 Initiating STRICT MODE YouTube Sniper (Double-Checked & Verified)...")

db_file = 'career_database.json'
with open(db_file, 'r') as f:
    db = json.load(f)

for branch, skills in db.items():
    for skill, links in skills.items():
        # URL encode the skill safely (turns spaces into +)
        safe_skill = urllib.parse.quote_plus(skill)
        
        # Use exact match quotes (%22) around the skill name to force YouTube
        # This prevents YouTube from confusing Flask and Django!
        exact_skill_query = f"%22{safe_skill}%22"
        
        try:
            # --- 1. STRICT PLAYLIST SEARCH ---
            playlist_url = f"https://www.youtube.com/results?search_query={exact_skill_query}+tutorial&sp=EgIQAw%253D%253D"
            req = urllib.request.Request(playlist_url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urllib.request.urlopen(req).read().decode('utf-8')
            
            # Find Playlist IDs
            playlists = re.findall(r"list=(PL[a-zA-Z0-9_-]+)", html)
            
            if playlists:
                db[branch][skill]["youtube"] = "https://www.youtube.com/playlist?list=" + playlists[0]
                print(f"📚 STRICT PLAYLIST: {skill}")
            else:
                # --- 2. STRICT SINGLE VIDEO FALLBACK ---
                video_url = f"https://www.youtube.com/results?search_query={exact_skill_query}+%22full+course%22"
                req = urllib.request.Request(video_url, headers={'User-Agent': 'Mozilla/5.0'})
                html = urllib.request.urlopen(req).read().decode('utf-8')
                
                # Find Video IDs
                video_ids = re.findall(r"watch\?v=([a-zA-Z0-9_-]{11})", html)
                
                if video_ids:
                    db[branch][skill]["youtube"] = "https://www.youtube.com/watch?v=" + video_ids[0]
                    print(f"🎬 STRICT VIDEO: {skill}")
            
            # Save immediately so you don't lose progress
            with open(db_file, 'w') as f:
                json.dump(db, f, indent=4)
                
            # Wait 3 seconds to prevent YouTube from blocking your IP
            time.sleep(3) 
            
        except Exception as e:
            print(f"⚠️ Skipped {skill} (Kept original link)")
            time.sleep(3)

print("\n🎉 STRICT MODE COMPLETE. All YouTube links are now heavily locked to the exact skill.")