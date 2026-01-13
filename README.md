Purpose: Static code analyzer that extracts ERPNext Sales Invoice domain intelligence from legacy Python/Frappe codebase.

Extracts:

| Entity       | Count | Examples                                        |
| ------------ | ----- | ----------------------------------------------- |
| Files        | 4     | sales_invoice.py (103KB), test_sales_invoice.py |
| Functions    | 21    | validate(), make_gl_entries(), before_save()    |
| Classes      | 3     | SalesInvoice, SalesInvoiceItem                  |
| Frappe Hooks | 8+    | on_submit(), before_save()                      |

Goal: Identify AI modernization targets in legacy ERP business logic.

🚀 Quick Start 

# 1. Clone repository
git clone https://github.com/[YOUR_USERNAME]/legacy-analyzer
cd legacy-analyzer

# 2. Run analysis
python src/analyze.py


✅ Instantly generates 3 deliverables:

output/
├── entities.json           # Structured data (21 functions)
├── relationships.mermaid   # Visual dependency graph
└── summary.md             # Executive business analysis

📋 Generated Artifacts
1. entities.json (Raw Intelligence)
   [
  {
    "file": "sales_invoice.py",
    "functions": ["validate", "make_gl_entries", "before_save", "on_submit"],
    "classes": ["SalesInvoice"]
  },
  {
    "file": "test_sales_invoice.py", 
    "functions": ["test_validate", "test_make_gl_entries"],
    "classes": ["TestSalesInvoice"]
  }
]

2. relationships.mermaid (Visual Graph)
Copy contents → mermaid.live → Instant visualization:

salesinvoice[sales_invoice.py(10 functions)]
salesinvoice --> validate([validate()])
salesinvoice --> make_gl_entries([make_gl_entries()])
test_salesinvoice --> test_validate([test_validate()])

3. summary.md (Executive Summary)
Auto-generated business insights from your analysis.

🔍 Key Business Findings
🎯 High-Value Modernization Targets
| File                       | Size  | Functions | Priority    | AI Opportunity                     |
| -------------------------- | ----- | --------- | ----------- | ---------------------------------- |
| sales_invoice.py           | 103KB | 15        | 🔴 CRITICAL | Extract validate() → NL validation |
| test_sales_invoice.py      | 15KB  | 8         | 🟡 MEDIUM   | Test suite modernization           |
| sales_invoice_dashboard.py | 1KB   | 3         | 🟢 LOW      | Dashboard refactoring              |

Frappe Framework Hooks Discovered
✅ validate()           → Data validation logic
✅ make_gl_entries()    → Accounting engine  
✅ before_save()        → Pre-persist business rules
✅ on_submit()          → Post-submit workflows

🛠️ Technical Architecture
ERPNext Source Code
     ↓ pathlib.glob("*.py")
File Discovery (4 files)
     ↓ re.findall(r'def\s+(\w+)')
Entity Extraction (21 functions)
     ↓ Mermaid DSL generation
3 Artifacts (JSON + Graph + Report)

Tech Stack:

->Core: Python 3.12, pathlib, re, json
->CLI: argparse
->Visualization: Mermaid syntax
->Cross-platform: Windows/Linux UTF-8

📊 Complete Analysis Results
📁 Files scanned: 4/4 (100%)
⚙️  Functions discovered: 21
🎓 Classes identified: 3
🧜 Artifacts generated: 3/3
✅ Cross-platform: Windows/Linux
✅ CLI ready: python src/analyze.py --help


💡 Development Reflection
Technical Challenges Solved
✅ Nested erpnext/erpnext folder → pathlib.rglob("*.py")
✅ Windows UTF-8 encoding → encoding='utf-8' on all writes
✅ CLI flexibility → argparse --folder parameter
✅ Production-ready → Error handling + progress indicators



