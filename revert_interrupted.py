import json
import urllib.parse

print("🩹 Initiating Surgical Revert for interrupted skills...")

# The exact 27 skills from your terminal output
INTERRUPTED_SKILLS = [
    "linear algebra", "calculus", "probability and statistics", "python programming",
    "data structures and algorithms", "numpy library", "pandas library", "scikit-learn",
    "supervised learning", "unsupervised learning", "deep learning", "neural networks architecture",
    "pytorch", "tensorflow", "natural language processing (nlp)", "computer vision",
    "reinforcement learning", "data preprocessing", "feature engineering", 
    "model evaluation and validation", "convolutional neural networks (cnn)", 
    "recurrent neural networks (rnn)", "transformers architecture", 
    "gradient descent optimization", "ensemble learning", "dimensionality reduction", "xgboost"
]

with open('career_database.json', 'r') as f:
    db = json.load(f)

fixed_count = 0

for branch, skills in db.items():
    for skill, links in skills.items():
        if skill.lower() in INTERRUPTED_SKILLS:
            safe_skill = urllib.parse.quote_plus(skill)
            
            # Apply the exact safe fallback logic you designed
            if branch in ["computer science", "electronics engineering", "information science"]:
                db[branch][skill]["reading"] = f"https://www.google.com/search?q=site%3Ageeksforgeeks.org+{safe_skill}"
            else:
                db[branch][skill]["reading"] = f"https://en.wikipedia.org/wiki/Special:Search?search={safe_skill}"
            
            print(f"✅ Reverted: {skill}")
            fixed_count += 1

with open('career_database.json', 'w') as f:
    json.dump(db, f, indent=4)

print("\n=========================================")
print("🎉 SURGICAL REVERT COMPLETE!")
print(f"➔ Successfully patched {fixed_count} interrupted skills.")
print("➔ Your database is safely restored to its pristine condition.")
print("=========================================")