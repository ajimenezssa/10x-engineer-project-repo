# PromptLab

**Your AI Prompt Engineering Platform**

---

## Welcome to the Team! 👋

Congratulations on joining the PromptLab engineering team! You've been brought on to help us build the next generation of prompt engineering tools.

### What is PromptLab?

PromptLab is an internal tool for AI engineers to **store, organize, and manage their prompts**. Think of it as a "Postman for Prompts" — a professional workspace where teams can:

- 📝 Store prompt templates with variables (`{{input}}`, `{{context}}`)
- 📁 Organize prompts into collections
- 🏷️ Tag and search prompts
- 📜 Track version history
- 🧪 Test prompts with sample inputs

### The Current Situation

The previous developer left us with a *partially working* backend. The core structure is there, but:

- There are **several bugs** that need fixing
- Some **features are incomplete**
- The **documentation is minimal** (you'll fix that)
- There are **no tests** worth mentioning
- **No CI/CD pipeline** exists
- **No frontend** has been built yet

Your job over the next 4 weeks is to transform this into a **production-ready, full-stack application**.

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ (for Week 4)
- Git

### Run Locally

```bash
# Clone the repo
git clone <your-repo-url>
cd promptlab

# Set up backend
cd backend
pip install -r requirements.txt
python main.py
```

API runs at: http://localhost:8000

API docs at: http://localhost:8000/docs

### Run Tests

```bash
cd backend
pytest tests/ -v
```

---

## Project Structure

```
promptlab/
├── README.md                    # You are here
├── PROJECT_BRIEF.md             # Your assignment details
├── GRADING_RUBRIC.md            # How you'll be graded
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api.py              # FastAPI routes
│   │   ├── models.py           # Pydantic models
│   │   ├── storage.py          # In-memory storage
│   │   └── utils.py            # Helper functions
│   │   └── tags.py             # New spec
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_api.py         # Basic tests
│   │   └── conftest.py         # Test fixtures
│   │   └── test_models.py      # Basic tests
│   │   └── test_storage.py     # Basic tests
│   │   └── test_tags.py        # Basic tests
│   │   └── test_utils.py       # Basic tests
│   ├── main.py                 # Entry point
│   └── requirements.txt
│
├── frontend/                    # You'll create this in Week 4
├── specs/                       # You'll create this in Week 2
├── docs/                        # You'll create this in Week 2
└── .github/                     # You'll set up CI/CD in Week 3
```

---

## Your Mission

### 🧪 Experimentation Encouraged!
While we provide guidelines, **you are the engineer**. If you see a better way to solve a problem using AI, do it!
- Want to swap the storage layer for a real database? **Go for it.**
- Want to add Authentication? **Do it.**
- Want to rewrite the API in a different style? **As long as tests pass, you're clear.**

The goal is to learn how to build *better* software *faster* with AI. Don't be afraid to break things and rebuild them better.

### Week 1: Fix the Backend
- Understand this codebase using AI
- Find and fix the bugs
- Implement missing features

### Week 2: Document Everything
- Write proper documentation
- Create feature specifications
- Set up coding standards

### Week 3: Make it Production-Ready
- Write comprehensive tests
- Implement new features with TDD
- Set up CI/CD and Docker

### Week 4: Build the Frontend
- Create a React frontend
- Connect it to the backend
- Polish the user experience

---

## API Endpoints (Current)

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/health` | Health check | ✅ Works |
| GET | `/prompts` | List all prompts | ⚠️ Has issues |
| GET | `/prompts/{id}` | Get single prompt | ❌ Bug |
| POST | `/prompts` | Create prompt | ✅ Works |
| PUT | `/prompts/{id}` | Update prompt | ⚠️ Has issues |
| DELETE | `/prompts/{id}` | Delete prompt | ✅ Works |
| GET | `/collections` | List collections | ✅ Works |
| GET | `/collections/{id}` | Get collection | ✅ Works |
| POST | `/collections` | Create collection | ✅ Works |
| DELETE | `/collections/{id}` | Delete collection | ❌ Bug |

---

## Tech Stack

- **Backend**: Python 3.10+, FastAPI, Pydantic
- **Frontend**: React, Vite (Week 4)
- **Testing**: pytest
- **DevOps**: Docker, GitHub Actions (Week 3)

---

## Need Help?

1. **Use AI tools** — This is an AI-assisted coding course!
2. Read the `PROJECT_BRIEF.md` for detailed instructions
3. Check `GRADING_RUBRIC.md` to understand expectations
4. Ask questions in the course forum

---

Good luck, and welcome to the team! 🚀
