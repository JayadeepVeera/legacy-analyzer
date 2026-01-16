from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import json
import os

app = FastAPI(title="ERPNext Modernizer API")

class AnalyzeRequest(BaseModel):
    folder: str = "erpnext/erpnext/accounts/doctype/sales_invoice"

@app.post("/modernize")
async def modernize(request: AnalyzeRequest):
    try:
        print(f"Starting modernization for: {request.folder}")
        
        # Call your analyzer CLI (SIMPLEST METHOD)
        result = subprocess.run(
            ["python", "src/analyze.py"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Analyzer failed: {result.stderr}")
        
        # Read results
        if os.path.exists("output/entities.json"):
            with open("output/entities.json", "r") as f:
                entities = json.load(f)
            files_analyzed = len(entities)
        else:
            files_analyzed = 0
            
        if os.path.exists("output/migrations.json"):
            with open("output/migrations.json", "r") as f:
                migrations = json.load(f)
            migrations_created = len(migrations)
        else:
            migrations_created = 0
            
        return {
            "status": "success",
            "message": "Modernization complete!",
            "files_analyzed": files_analyzed,
            "migrations_created": migrations_created,
            "files": ["entities.json", "migrations.json"],
            "analyzer_output": result.stdout[-500:]  # Last 500 chars
        }
        
    except Exception as e:
        print(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "ERPNext Modernizer API is live!",
        "endpoints": ["/modernize (POST)", "/docs (Swagger UI)"],
        "run_pipeline": "POST to /modernize"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "analyzer_ready": os.path.exists("src/analyze.py")}
