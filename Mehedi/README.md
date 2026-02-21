# Aura - AI Student OS

UK-focused AI educational platform with Socratic questioning and career guidance.

## Tech Stack

- **FastAPI** - Modern Python web framework
- **Gemini 1.5 Pro** - Google's generative AI (via google-generativeai)
- **ElevenLabs** - Voice streaming API
- **python-dotenv** - Environment variable management

## Project Structure

```
Mehedi/
├── backend/
│   ├── config.py           # Centralized Gemini + API key configuration
│   ├── main.py             # FastAPI application
│   └── __init__.py
├── intelligence/
│   ├── socratic_engine.py  # Socratic questioning engine
│   ├── career_matcher.py   # UK job description analyzer
│   ├── integrity_guard.py  # Academic integrity checker
│   ├── chunker.py          # Text chunking utilities
│   └── __init__.py
├── voice/
│   ├── eleven_stream.py    # ElevenLabs streaming
│   └── __init__.py
├── prompts/
│   ├── socratic_viva.txt   # Socratic prompt template
│   └── career_analysis.txt # Career analysis prompt
├── requirements.txt
└── .env.example
```

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   - `GEMINI_API_KEY` - From Google AI Studio
   - `ELEVEN_LABS_API_KEY` - From ElevenLabs dashboard

3. **Run the server**
   ```bash
   cd backend
   python main.py
   ```
   
   Or with uvicorn:
   ```bash
   uvicorn backend.main:app --reload
   ```

## API Endpoints

### POST `/socratic`
Generates Socratic questions using UK Russell Group methodology.

**Request:**
```json
{
  "topic": "recursion in Python",
  "previous_answer": "optional student response"
}
```

**Response:**
```json
{
  "question": "Rather than providing a definition, consider: what happens when a function references itself?"
}
```

### POST `/career-analysis`
Analyzes UK job descriptions and extracts structured requirements.

**Request:**
```json
{
  "job_text": "We are seeking a Graduate Software Engineer..."
}
```

**Response:**
```json
{
  "technical_skills": ["Python", "RESTful APIs"],
  "tools_technologies": ["Git", "Docker"],
  "cognitive_skills": ["Problem-solving", "Analytical thinking"],
  "behavioural_traits": ["Team collaboration", "Communication"],
  "experience_level": "Graduate / Entry-level"
}
```

## Architecture Principles

- **Fail fast** - API keys validated at startup
- **Clean separation** - Config, intelligence, and voice modules are independent
- **Safe JSON parsing** - Handles markdown-wrapped and malformed JSON
- **Low temperature** - 0.2 for extraction, 0.4 for questioning
- **UK-focused** - Russell Group academic standards
- **No cheating** - Socratic method prevents direct answer provision

## Temperature Settings

- **Career analysis**: 0.2 (deterministic extraction)
- **Socratic engine**: 0.4 (consistent but creative questioning)
- **Integrity guard**: 0.1 (strict classification)

## Security

- API keys loaded from `.env` (never hardcoded)
- Validation on startup prevents silent failures
- Academic integrity checking on student queries
