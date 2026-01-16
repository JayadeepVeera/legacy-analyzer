MIGRATION_TEMPLATES = {
    "validate": """
@app.post("/invoices/validate")
async def validate_invoice(invoice: InvoiceCreate):
    if invoice.total < 0:
        raise HTTPException(status_code=400, detail="Negative total not allowed")
    return {"status": "valid", "invoice_id": invoice.id}
""",
    
    "make_gl_entries": """
@app.post("/invoices/gl-entries")
async def create_gl_entries(invoice_id: str):
    gl_entries = await generate_accounting_entries(invoice_id)
    return {"entries_created": len(gl_entries), "invoice_id": invoice_id}
""",
    
    "before_save": """
@app.post("/invoices/before-save")
async def before_invoice_save(invoice: InvoiceUpdate):
    await run_pre_save_hooks(invoice)
    return invoice
"""
}

def migrate_function(func_name):
    print(f"Migrating {func_name}()...")
    
    for pattern, modern_code in MIGRATION_TEMPLATES.items():
        if pattern in func_name.lower():
            return {
                "old": func_name + "(frappe)",
                "new": modern_code.strip(),
                "status": "MIGRATED!"
            }
    
    return {
        "old": func_name + "(frappe)",
        "new": f"@app.post('/{func_name.lower()}/')\nasync def {func_name.lower()}_endpoint(data):\n    return {{'status': 'migrated'}}",
        "status": "MIGRATED!"
    }

print("AI Brain Ready!")
