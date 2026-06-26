# Lexora

AI-Powered RAG Document QA System. Upload documents, ask questions, get answers with source citations.

## Tech Stack

- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Zustand
- **Backend**: Python, FastAPI, Google Gemini, SQLAlchemy
- **Database**: PostgreSQL (Neon)
- **Vector DB**: FAISS
- **Auth**: JWT

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
