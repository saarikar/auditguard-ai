from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

class FlaggedClause(BaseModel):
    clause_title: str
    risk_level: str  # HIGH, MEDIUM, LOW
    reason: str

class AuditResponse(BaseModel):
    filename: str
    overall_confidence: float
    flagged_clauses: List[FlaggedClause]

@app.post("/audit", response_model=AuditResponse)
async def audit_document(file: UploadFile = File(...)):
    # Mocking real LlamaIndex / Agentic RAG evaluation output
    # Replace this block with your actual RAG parser call
    return AuditResponse(
        filename=file.filename,
        overall_confidence=0.78,  # Below 0.90 threshold to test HITL workflow
        flagged_clauses=[
            FlaggedClause(
                clause_title="Indemnity & Liability",
                risk_level="HIGH",
                reason="Uncapped liability limits detected in Section 4.2."
            )
        ]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
