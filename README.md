# AI Resume Analyzer + Job Matcher

Full-stack application to analyze a resume PDF against a job description and return a structured match report.

## Features
- Upload resume PDF
- Analyze resume against job description using OpenAI with LangChain orchestration
- Returns match percentage, matching skills, missing skills, verdict, and suggestions
- Includes model fallback, Redis caching, latency logging, and structured logging
- Production-ready with Docker, health checks, and proper error handling

## Quick Start (Development)

### Prerequisites
- Python 3.11+
- Node.js 18+
- Redis (for caching)

### Backend Setup

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy environment file and configure:
   ```bash
   cp ../.env.example .env
   # Edit .env with your OpenAI API key
   ```

4. Start Redis (if not running):
   ```bash
   # Using Docker
   docker run -d -p 6379:6379 redis:7-alpine
   ```

5. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the React app:
   ```bash
   npm run dev
   ```

## Production Deployment

### Using Docker Compose

1. Copy and configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your production settings
   ```

2. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

The application will be available at `http://localhost:8000` with Redis caching enabled.

### Manual Production Setup

1. Install Redis server
2. Set environment variables:
   ```bash
   export ENVIRONMENT=production
   export REDIS_URL=redis://localhost:6379
   export LOG_LEVEL=INFO
   ```
3. Run with uvicorn:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

### Endpoints
- `POST /upload` - Upload and extract text from PDF
- `POST /analyze` - Analyze resume against job description
- `GET /health` - Health check endpoint

## 🚀 Production-Grade Features Implemented

### ✅ Completed Improvements
- **Redis Caching**: Distributed caching with Redis instead of in-memory
- **Structured Logging**: JSON logging with latency tracking using structlog
- **Latency Logging**: Request/response time monitoring
- **Docker Support**: Containerization with health checks
- **Environment Configuration**: Comprehensive settings management
- **Error Handling**: Proper HTTP status codes and exception handling
- **Security**: Non-root user execution in containers

### 🔄 LangChain Integration (Ready for Implementation)
LangChain dependencies are prepared in `requirements.txt` (commented out). To enable:

1. Uncomment LangChain lines in `requirements.txt`:
   ```bash
   pip install langchain==0.1.20 langchain-openai==0.1.6
   ```

2. Update `backend/services/llm_service.py` to use LangChain PromptTemplate and LLMChain

3. The current implementation uses direct OpenAI API calls for stability

## 🏗️ Architecture Overview

```
AI Resume Analyzer
├── Backend (FastAPI)
│   ├── Services
│   │   ├── LLM Service (OpenAI + fallback)
│   │   └── PDF Service (text extraction)
│   ├── Utils
│   │   ├── Config (Pydantic settings)
│   │   ├── Cache (Redis-based)
│   │   └── Logger (structured logging)
│   └── Routes
│       └── Analyze (resume-job matching)
├── Frontend (React)
└── Infrastructure
    ├── Docker (containerization)
    ├── Redis (caching)
    └── docker-compose (orchestration)
```

## Configuration

All configuration is handled via environment variables in the `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key
- `DEFAULT_MODEL`: Primary LLM model (default: gpt-4o-mini)
- `FALLBACK_MODEL`: Backup model (default: gpt-3.5-turbo)
- `CACHE_TTL_SECONDS`: Cache expiration time (default: 300)
- `REDIS_URL`: Redis connection URL (default: redis://localhost:6379)
- `LOG_LEVEL`: Logging level (default: INFO)
- `ENVIRONMENT`: Environment mode (development/production)

## Monitoring

The application includes comprehensive logging for monitoring:
- Request latency tracking
- LLM call performance
- Cache hit/miss ratios
- Error rates and types

Logs are structured as JSON in production for easy parsing by log aggregation tools.
- Open the frontend URL shown by Vite (usually `http://localhost:5173`)
- Upload a PDF resume
- Paste a job description
- Click `Analyze Resume`

## Notes
- The backend is configured for CORS from any origin for local development.
- If the OpenAI API fails with the primary model, the backend attempts a fallback.
- Analysis results are cached for repeated identical requests for 5 minutes.
