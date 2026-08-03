# ⚡ AI-Powered Resume Screener & Candidate Outreach System

An automated, end-to-end recruitment pipeline that processes resumes, extracts technical skills, ranks candidates against job requirements, and features a RAG-based Conversational AI for deep candidate analysis.

**Lead Developer:** Manav Singh  
**Role:** Conversational AI Engineer / Cognitive Developer Intern @ EXL  
**Education:** Chitkara University

---

## 🚀 Key Features

- **Automated Parsing:** Extracts raw text, emails, education, and experience from PDF/DOCX resumes.
- **Intelligent Scoring:** Calculates a match percentage against target job descriptions.
- **Interactive Dashboard:** Filter candidates by skills, experience, and match score using a sleek Streamlit UI.
- **Conversational AI (RAG):** Chat directly with a candidate's resume to generate custom interview questions and verify expertise.
- **Automated Outreach:** One-click background tasks to queue and send interview invitation emails.

## 🛠️ Tech Stack

- **Frontend:** Streamlit (Python)
- **Backend:** FastAPI, Uvicorn, Python 3.10
- **AI/LLM:** Google Gemini 1.5 Flash (`google-genai` SDK)
- **Database:** SQLite / SQLAlchemy
- **Infrastructure:** Docker & Docker Compose

---

## 💻 Local Setup & Quick Start

### 1. Clone the Repository

```bash
git clone [https://github.com/YOUR_USERNAME/ai-resume-screener.git](https://github.com/YOUR_USERNAME/ai-resume-screener.git)
cd ai-resume-screener
```

### 2. Configure Environment Variables

```
In the app/dashboard.py file, ensure you have inserted your Google AI Studio Authentication Key:
client = genai.Client(api_key="YOUR_AQ_KEY_HERE")

```

### 3. Run with Docker

```
The entire application is containerized. Build and start the services with one command in vs code:

docker-compose up --build

```

### 4. Access the Application

Frontend Dashboard: http://localhost:8501

Backend API Docs: http://localhost:8000/docs

### 📂 Project Structure

/app - Core FastAPI backend logic, routers, and database models.

/dashboard.py - Streamlit frontend interface.

docker-compose.yml - Multi-container orchestration.

API.md - Core API endpoint documentation.

SCHEMA.md - Database table architecture.

/sample_data - Test resumes for evaluation.
