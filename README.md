# AI Resume Analyzer + Job Matcher

Full-stack application to analyze a resume PDF against a job description and return a structured match report.

## Features
- Upload resume PDF
- Analyze resume against job description using OpenAI
- Returns match percentage, matching skills, missing skills, verdict, and suggestions
- Includes model fallback, caching, and token usage tracking

## Backend Setup

1. Navigate to the backend folder:
   ```bash
   cd "c:\Users\satya\OneDrive\Desktop\AI project\backend"
   ```

2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. Create a `.env` file in `backend/` with this content:
   ```text
   OPENAI_API_KEY=your_openai_api_key
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Frontend Setup

1. Navigate to the frontend folder:
   ```bash
   cd "c:\Users\satya\OneDrive\Desktop\AI project\frontend"
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the React app:
   ```bash
   npm run dev
   ```

## Usage
- Open the frontend URL shown by Vite (usually `http://localhost:5173`)
- Upload a PDF resume
- Paste a job description
- Click `Analyze Resume`

## Notes
- The backend is configured for CORS from any origin for local development.
- If the OpenAI API fails with the primary model, the backend attempts a fallback.
- Analysis results are cached for repeated identical requests for 5 minutes.
