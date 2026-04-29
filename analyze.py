import time
from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from backend.services.pdf_service import extract_text_from_pdf
from backend.services.llm_service import analyze_resume_against_job
from backend.utils.cache import get_cached_analysis, set_cached_analysis
from backend.utils.config import settings
from backend.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """Test endpoint for uploading PDF resumes and verifying text extraction."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    try:
        raw_text = await extract_text_from_pdf(file)
        return {"filename": file.filename, "extracted_text": raw_text[:500], "full_text_length": len(raw_text)}
    except Exception as exc:
        logger.exception("Failed to extract resume text", extra={"filename": file.filename})
        raise HTTPException(status_code=500, detail="Resume extraction failed.")


@router.post("/analyze")
async def analyze_resume(job_description: str = Form(...), resume_file: UploadFile = File(...)):
    """Analyze a resume against a job description and return structured analysis."""
    if resume_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF resumes are accepted.")

    start_time = time.perf_counter()
    try:
        resume_text = await extract_text_from_pdf(resume_file)
        cache_key = f"{resume_text[:1000]}|{job_description[:1000]}"
        cached = get_cached_analysis(cache_key)
        if cached:
            logger.info("Returning cached analysis result", extra={"filename": resume_file.filename})
            return JSONResponse(content=cached)

        analysis = await analyze_resume_against_job(resume_text, job_description)
        set_cached_analysis(cache_key, analysis, ttl=settings.CACHE_TTL_SECONDS)

        total_latency = time.perf_counter() - start_time
        analysis["total_latency_ms"] = round(total_latency * 1000, 2)

        logger.info(
            "Analysis completed",
            extra={
                "filename": resume_file.filename,
                "match_percentage": analysis.get("match_percentage"),
                "verdict": analysis.get("verdict"),
                "total_latency_ms": analysis["total_latency_ms"],
            }
        )

        return JSONResponse(content=analysis)

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error while analyzing resume", extra={"filename": resume_file.filename})
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again later.")
    finally:
        elapsed = time.perf_counter() - start_time
        logger.info("Request processed", extra={"path": "/analyze", "duration_seconds": elapsed})
