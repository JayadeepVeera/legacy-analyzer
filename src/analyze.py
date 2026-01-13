import re
import os
import json
from pathlib import Path
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="ERPNext Sales Invoice Code Analyzer")
    parser.add_argument("--folder", default="erpnext/erpnext/accounts/doctype/sales_invoice", 
                        help="Target folder to analyze")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--limit", type=int, default=10, help="Max functions per file")
    return parser.parse_args()

def find_py_files(folder_path):
    full_path = os.path.abspath(folder_path)
    print(f"🔍 Scanning: {full_path}")
    
    path = Path(full_path)
    py_files = list(path.rglob("*.py"))
    
    print(f"📁 Found {len(py_files)} files:")
    for f in py_files[:3]:
        print(f"   📄 {f.name}")
    return [str(f) for f in py_files]

def extract_entities(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    functions = re.findall(r'def\s+(\w+)', content)
    classes = re.findall(r'class\s+(\w+)', content)
    
    return {
        'file': os.path.basename(file_path),
        'path': file_path,
        'functions': list(set(functions))[:10],
        'classes': list(set(classes))
    }

def create_mermaid_diagram(entities):
    """Generate Mermaid diagram showing file → function relationships"""
    mermaid = "graph TD\n"
    
    # File nodes (boxes)
    for entity in entities:
        file_short = entity['file'].replace('.py', '')
        mermaid += f"    {file_short}[{entity['file']}]"
        mermaid += f"({len(entity['functions'])} functions)\n"
    
    # File → Function relationships
    mermaid += "\n"
    for entity in entities:
        file_short = entity['file'].replace('.py', '')
        for func in entity['functions'][:5]:
            mermaid += f"    {file_short} --> {func}([{func}])\n"
    
    return mermaid

def create_summary_report(entities):
    """Generate human-readable summary for README"""
    total_files = len(entities)
    total_funcs = sum(len(e['functions']) for e in entities)
    total_classes = sum(len(e['classes']) for e in entities)
    
    summary = f"# Sales Invoice Code Analysis\n\n"
    summary += f"**Analyzed {total_files} files, {total_funcs} functions, {total_classes} classes**\n\n"
    summary += "## Key Files\n\n"
    
    # Top files by function count
    top_files = sorted(entities, key=lambda x: len(x['functions']), reverse=True)[:5]
    for entity in top_files:
        summary += f"### {entity['file']}\n"
        summary += f"- **{len(entity['functions'])} functions**\n"
        summary += f"- Sample: `{', '.join(entity['functions'][:3])}`\n\n"
    
    summary += "## Business Logic Functions Found\n\n"
    business_funcs = {}
    for entity in entities:
        for func in entity['functions']:
            if any(x in func.lower() for x in ['validate', 'make_', 'check_', 'get_', 'set_']):
                business_funcs.setdefault(entity['file'], []).append(func)
    
    for file, funcs in list(business_funcs.items())[:3]:
        summary += f"**{file}:** `{', '.join(funcs[:3])}`\n"
    
    summary += f"\n**Full data:** [entities.json](output/entities.json)"
    return summary

def main():
    args = parse_args()
    target_folder = args.folder  # FIXED: Use CLI argument
    
    print(f"🚀 Analyzing: {target_folder}")
    files = find_py_files(target_folder)
    
    print(f"\nAnalyzing {len(files)} files...")
    
    # ANALYZE EVERY FILE
    all_entities = []
    for file_path in files:
        entity = extract_entities(file_path)
        all_entities.append(entity)
    
    # CREATE ALL 3 DELIVERABLES
    Path("output").mkdir(exist_ok=True)
    
    # 1. JSON with ALL data
    with open("output/entities.json", 'w', encoding='utf-8') as f:
        json.dump(all_entities, f, indent=2)
    
    # 2. Mermaid diagram
    mermaid = create_mermaid_diagram(all_entities)
    with open("output/relationships.mermaid", 'w', encoding='utf-8') as f:
        f.write(mermaid)
    
    # 3. Summary report
    summary = create_summary_report(all_entities)
    with open("output/summary.md", 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"\n✅ COMPLETE! Generated 3 artifacts:")
    print(f"   📊 output/entities.json     ({len(all_entities)} files)")
    print(f"   🧜 output/relationships.mermaid")
    print(f"   📝 output/summary.md")
    
    print(f"\n📈 STATS:")
    total_funcs = sum(len(e['functions']) for e in all_entities)
    total_classes = sum(len(e['classes']) for e in all_entities)
    print(f"   Functions: {total_funcs}")
    print(f"   Classes:   {total_classes}")
    print(f"\n🎯 Test Mermaid: https://mermaid.live")

if __name__ == "__main__":
    main()
