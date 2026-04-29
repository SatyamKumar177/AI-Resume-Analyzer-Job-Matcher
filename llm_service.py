import json
import time
from typing import Dict, Any
from openai import OpenAI
from backend.utils.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Initialize client lazily
_client = None

def get_openai_client():
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client

PROMPT_TEMPLATE = """
You are an AI resume analyst. Compare the candidate resume text with the target job description.
Produce a strict JSON object with the following fields:
- match_percentage: integer between 0 and 100
- matching_skills: list of skills or keywords found in both resume and description
- missing_skills: list of skills or keywords present in the job description but missing from the resume
- verdict: one of ["Strong", "Moderate", "Weak"]
- suggestions: a concise paragraph with improvement suggestions for the candidate

Respond with JSON only.

Resume:
{resume}

Job Description:
{job_description}
"""

MODEL_PREFERENCES = [settings.DEFAULT_MODEL, settings.FALLBACK_MODEL]


def _build_messages(resume: str, job_description: str) -> str:
    return PROMPT_TEMPLATE.format(resume=resume, job_description=job_description)


def _parse_response(response_text: str) -> dict:
    """Extract JSON object from model response and convert it into Python types."""
    try:
        payload = json.loads(response_text)
    except json.JSONDecodeError:
        start = response_text.find("{")
        end = response_text.rfind("}")
        if start == -1 or end == -1:
            raise
        payload = json.loads(response_text[start:end+1])

    return {
        "match_percentage": int(payload.get("match_percentage", 0)),
        "matching_skills": payload.get("matching_skills", []),
        "missing_skills": payload.get("missing_skills", []),
        "verdict": payload.get("verdict", "Weak"),
        "suggestions": payload.get("suggestions", ""),
    }


async def analyze_resume_against_job(resume_text: str, job_description: str) -> Dict[str, Any]:
    """Call the LLM to analyze the resume, with a fallback model if the first attempt fails."""
    last_error = None

    for model in MODEL_PREFERENCES:
        try:
            logger.info("Calling LLM model", extra={"model": model})

            start_time = time.perf_counter()
            response = get_openai_client().chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": _build_messages(resume_text, job_description)}],
                temperature=0.0,
                max_tokens=450,
            )
            latency = time.perf_counter() - start_time

            logger.info("LLM call completed", extra={"model": model, "latency_ms": round(latency * 1000, 2)})

            text = response.choices[0].message.content
            result = _parse_response(text)

            # Add latency to result
            result["latency_ms"] = round(latency * 1000, 2)

            return result

        except Exception as error:
            last_error = error
            logger.warning("LLM model failed, trying fallback", extra={"model": model, "error": str(error)})

    logger.error("All LLM models failed", exc_info=last_error)
    raise RuntimeError("LLM service unavailable")
    """Call the LLM to analyze the resume, with a fallback model if the first attempt fails."""
    prompt = _build_messages(resume_text, job_description)
    last_error = None

    for model in MODEL_PREFERENCES:
        try:
            logger.info("Calling LLM model", extra={"model": model})
            response = client.responses.create(
                model=model,
                input=prompt,
                temperature=0.0,
                max_output_tokens=450,
            )

            text = response.output_text
            result = _parse_response(text)
            usage = getattr(response, "usage", None)
            if usage:
                result["token_usage"] = {
                    "prompt_tokens": usage.get("prompt_tokens"),
                    "completion_tokens": usage.get("completion_tokens"),
                    "total_tokens": usage.get("total_tokens"),
                }
            return result

        except Exception as error:
            last_error = error
            logger.warning("LLM model failed, trying fallback", extra={"model": model, "error": str(error)})

    logger.error("All LLM models failed", exc_info=last_error)
    raise RuntimeError("LLM service unavailable")
