import json
import urllib.request
import re
import time
import os

print("Starting the Ultra-Safe YouTube Sniper...")

# 1. Load your current database
db_file = 'career_database.json'
with open(db_file, 'r') as f:
    db = json.load(f)

total_playlists = 0
total_videos = 0

for branch, skills in db.items():
    for skill, links in skills.items():
        yt_link = links.get("youtube", "")
        
        # If it's a search link, let's fix it!
        if "search_query" in yt_link:
            try:
                search_term = yt_link.split('=')[1]
                
                # STEP 1: Search for PLAYLISTS
                playlist_url = "https://www.youtube.com/results?search_query=" + search_term + "&sp=EgIQAw%253D%253D"
                req = urllib.request.Request(playlist_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                html = urllib.request.urlopen(req).read().decode('utf-8')
                
                playlists = re.findall(r"list=(PL[a-zA-Z0-9_-]+)", html)
                
                if playlists:
                    exact_link = "https://www.youtube.com/playlist?list=" + playlists[0]
                    db[branch][skill]["youtube"] = exact_link
                    total_playlists += 1
                    print(f"📚 PLAYLIST: {skill} -> {exact_link}")
                else:
                    # STEP 2: Fallback to a single "Full Course" video
                    video_url = "https://www.youtube.com/results?search_query=" + search_term + "+full+course"
                    req = urllib.request.Request(video_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                    html = urllib.request.urlopen(req).read().decode('utf-8')
                    
                    video_ids = re.findall(r"watch\?v=([a-zA-Z0-9_-]{11})", html)
                    if video_ids:
                        exact_link = "https://www.youtube.com/watch?v=" + video_ids[0]
                        db[branch][skill]["youtube"] = exact_link
                        total_videos += 1
                        print(f"🎬 VIDEO: {skill} -> {exact_link}")
                
                # 💾 SAFETY NET: Save the file immediately after every single fix
                with open(db_file, 'w') as f:
                    json.dump(db, f, indent=4)
                    
                # 🐢 SAFETY NET: Sleep for 4 full seconds to perfectly mimic a human
                time.sleep(4) 
                
            except Exception as e:
                print(f"⚠️ Skipped {skill} (Will keep original search link).")
                time.sleep(4) # Still sleep on errors to be safe!

print(f"\n🎉 DONE! Safely upgraded {total_playlists} Playlists and {total_videos} Videos.")