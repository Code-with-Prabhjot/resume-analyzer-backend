from app import CAREER_DB

def generate_hardened_roadmap(missing_skills):
    if not missing_skills:
        return {} 

    phases = [
        {"phase": "Phase 1: Basics", "skills": []},
        {"phase": "Phase 2: Intermediate", "skills": []},
        {"phase": "Phase 3: Advanced", "skills": []},
        {"phase": "Phase 4: Project & Practice", "skills": []}
    ]

    for i, skill in enumerate(missing_skills):
        phase_index = i % 4
        phases[phase_index]["skills"].append(skill)

    game_plan = {}
    
    for phase in phases:
        if not phase["skills"]:
            continue 

        phase_tasks = []
        
        for skill in phase["skills"]:
            # 💥 Phase 4 Hardening: Append terms to ensure high-quality, comprehensive learning resources
            skill_query = skill.replace(" ", "+")
            links = {
                "youtube": f"https://www.youtube.com/results?search_query={skill_query}+full+course+playlist",
                "course": f"https://www.coursera.org/search?query={skill_query}+tutorial",
                "reading": f"https://www.google.com/search?q={skill_query}+documentation+tutorial"
            }
            
            # If the database provides curated links, prefer them (they are assumed to be already high-quality)
            for branch, branch_skills in CAREER_DB.items():
                if skill in branch_skills:
                    links["youtube"] = branch_skills[skill].get("youtube", links["youtube"])
                    links["course"] = branch_skills[skill].get("course", links["course"])
                    links["reading"] = branch_skills[skill].get("reading", links["reading"])
                    break 
            
            phase_tasks.append({
                "skill_name": f"Learn {skill.title()}",
                "links": links
            })

        game_plan[phase["phase"]] = phase_tasks 
        
    return game_plan
