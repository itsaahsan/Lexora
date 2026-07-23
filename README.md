# Lexora

AI-Powered RAG Document QA System. Upload documents, ask questions, get answers with source citations.

## Live Demo

- **App**: https://lexora-blond-delta.vercel.app
- **API Docs**: https://lexora-blond-delta.vercel.app/api/docs

## Tech Stack

- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Zustand
- **Backend**: Python, FastAPI, Google Gemini, SQLAlchemy
- **Database**: PostgreSQL (Neon)
- **Vector DB**: FAISS
- **Auth**: JWT
- **Deployment**: Vercel (Serverless)

## Project Structure

```
Lexora/
├── api/                  # Vercel serverless API (FastAPI + Mangum)
├── frontend/             # React SPA (Vite)
├── vercel.json           # Vercel routing config
└── .github/workflows/    # CI pipeline
```

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
cd api
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

**api/.env**
```
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=your-secret-key
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
FAISS_INDEX_PATH=./faiss_index
UPLOAD_DIR=./uploads
ALLOWED_ORIGINS=["http://localhost:5173"]
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
| PUT | /api/auth/profile | Update profile |
| POST | /api/documents/upload | Upload document |
| GET | /api/documents | List documents |
| GET | /api/documents/{id} | Get document |
| DELETE | /api/documents/{id} | Delete document |
| POST | /api/chat | Send message |
| GET | /api/conversations | List conversations |
| GET | /api/conversations/{id}/messages | Get messages |
| DELETE | /api/conversations/{id} | Delete conversation |
| GET | /api/analytics/overview | Analytics overview |
| GET | /api/analytics/documents | Document analytics |

## Deployment

### Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

Or connect your GitHub repo to Vercel for automatic deployments.

## License

MIT

## Author

**Amimul Ahsan** - [GitHub](https://github.com/itsaahsan)
