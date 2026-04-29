from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.analyze import router as analyze_router
from backend.utils.logger import configure_logging

app = FastAPI(
    title="AI Resume Analyzer + Job Matcher",
    description="Analyze a resume PDF against a job description and return a structured fit score.",
    version="1.0.0",
)

configure_logging()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router, prefix="", tags=["analysis"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
