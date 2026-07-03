# Lexora

AI-Powered RAG Document QA System. Upload documents, ask questions, get answers with source citations.

## Live Demo

- **App**: https://lexora-xtgo.onrender.com
- **API Docs**: https://lexora-xtgo.onrender.com/docs

> Hosted on Render's free tier — the first request after inactivity may take a few seconds to spin up.

## Tech Stack

- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Zustand
- **Backend**: Python, FastAPI, Google Gemini, SQLAlchemy
- **Database**: PostgreSQL (Neon)
- **Vector DB**: FAISS
- **Auth**: JWT

## Why These Choices

- **FAISS over a managed vector DB** — keeps the retrieval layer self-hosted and free-tier friendly, since Pinecone/Weaviate-style managed services add cost and an external dependency that isn't needed at this scale.
- **Gemini over OpenAI** — free-tier API access made it practical to iterate on prompt and chunking strategy without hitting cost limits during development.
- **Source citations returned with every answer** — RAG systems are only trustworthy if a user can verify where an answer came from, so citations aren't an add-on, they're part of the core response contract.

## Quick Start

### Docker (Recommended)
```bash
docker-compose up --build
```
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs

### Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

**backend/.env**
```
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=your-secret-key
GEMINI_API_KEY=your-gemini-api-key
```

**frontend/.env**
```
VITE_API_URL=http://localhost:8000/api
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register |
| POST | /api/auth/login | Login |
| GET | /api/auth/me | Current user |
| POST | /api/documents/upload | Upload document |
| GET | /api/documents | List documents |
| DELETE | /api/documents/{id} | Delete document |
| POST | /api/chat | Send message |
| GET | /api/conversations | List conversations |
| GET | /api/analytics/overview | Analytics |

## License

MIT

## Author

**Amimul Ahsan** - [GitHub](https://github.com/itsaahsan)
