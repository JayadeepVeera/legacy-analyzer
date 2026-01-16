import json
import os

def find_errors():
    print("Reading analyzer results...")
    
    with open("output/entities.json", "r") as f:
        files = json.load(f)
    
    problems = []
    danger_words = ["validate", "make_gl", "before_save", "frappe.db.sql", "loop"]
    
    for file_info in files:
        filename = file_info["file"]
        functions = file_info["functions"]
        
        for func_name in functions:
            for danger in danger_words:
                if danger in func_name.lower():
                    problems.append({
                        "file": filename,
                        "danger_function": func_name,
                        "problem": f"'{danger}' = NEEDS MODERNIZATION!"
                    })
    
    print(f"Found {len(problems)} modernization targets!")
    return problems

def find_real_code_problems():
    print("Reading REAL code...")
    
    with open("output/entities.json", "r") as f:
        files = json.load(f)
    
    real_problems = []
    
    for file_info in files:
        try:
            filepath = file_info["path"]
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    code = f.read()
                
                if "frappe.db.sql" in code:
                    real_problems.append({
                        "file": file_info["file"],
                        "problem": "RAW SQL DETECTED! (SQL Injection risk)"
                    })
                if "for item in" in code and "frappe.get_all" in code:
                    real_problems.append({
                        "file": file_info["file"],
                        "problem": "N+1 QUERY PROBLEM! (Performance)"
                    })
        except Exception as e:
            print(f"Skip {file_info['file']}: {e}")
            continue
    
    print(f"Found {len(real_problems)} real code issues!")
    return real_problems

if __name__ == "__main__":
    find_errors()
    find_real_code_problems()
