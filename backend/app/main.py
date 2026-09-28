"""
FORGE FastAPI Main Application Entry Point
Initializes DB tables, seeds datasets, enables CORS, and includes REST API router.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.api.routes import router, DEMO_FULL_ANALYSIS_SCRIPT, execute_script, ScriptExecuteRequest
from app.seed import seed_datasets
from app.models.models import CaseModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create DB tables
    Base.metadata.create_all(bind=engine)

    # Seed synthetic datasets
    seed_datasets()

    # Pre-seed initial CASE-001 and execute initial demo run if DB empty
    db = SessionLocal()
    try:
        case = db.query(CaseModel).filter(CaseModel.case_id == "CASE-001").first()
        if not case:
            case = CaseModel(
                case_id="CASE-001",
                title="SIH26148 Digital Forensic Incident Response",
                description="Controlled computer and network forensic investigation against endpoint and PCAP datasets.",
                analyst_id="investigator@org.example",
                status="ACTIVE"
            )
            db.add(case)
            db.commit()

            # Execute initial baseline demo run
            req = ScriptExecuteRequest(
                script_id="SCR-DEMO-INIT",
                source_code=DEMO_FULL_ANALYSIS_SCRIPT,
                case_id="CASE-001",
                analyst_id="investigator@org.example"
            )
            execute_script(req, db)
    finally:
        db.close()

    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="SIH26148 FORGE — Forensic Object Runtime & Governed Execution Platform",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "Welcome to FORGE — Forensic Object Runtime & Governed Execution API",
        "health": "/api/v1/health",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
