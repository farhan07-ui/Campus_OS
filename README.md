# 🎓 CampusOS - AI Powered Campus Operating System

CampusOS is a **Full-Stack AI-powered University Management Platform** that leverages **Large Language Models (LLMs)** and a **Multi-Agent Architecture** to simplify academic workflows for students. The platform combines intelligent AI agents with modern web technologies to provide personalized academic assistance through a unified interface.

This repository contains the **Phase 1 (30% Implementation)** of the project, focusing on four core AI agents:
- 📚 Syllabus Chat Agent
- 📝 Assignment Assistant Agent
- 📅 AI Timetable Generator
- 📄 AI Resume Builder

---

## 🚀 Features

### 📚 Syllabus Chat Agent
- Upload syllabus PDF
- Ask questions about the syllabus
- Retrieval-Augmented Generation (RAG)
- Semantic search using Vector Database
- AI-powered explanations

### 📝 Assignment Assistant
- Upload assignment files
- AI-generated summary
- Assignment explanation
- Task checklist generation
- Estimated completion time
- Learning resource suggestions

### 📅 AI Timetable Generator
- Generate personalized study timetable
- Organize subjects and study hours
- Balanced weekly schedule
- Easy-to-read timetable output

### 📄 Resume Builder
- Generate professional resumes
- AI-assisted resume writing
- ATS-friendly formatting
- PDF export support

---

# 🏗️ Project Architecture

```
                 User
                   │
                   ▼
            React Frontend
                   │
                   ▼
            FastAPI Backend
                   │
          LangGraph Supervisor
                   │
    ┌────────┬────────┬────────┬────────┐
    ▼        ▼        ▼        ▼
Syllabus Assignment Resume Timetable
 Agent      Agent     Agent     Agent
    │        │         │         │
    └────────┴─────────┴─────────┘
                   │
                   ▼
           Gemini / OpenAI / Groq
                   │
      PostgreSQL + Vector Database
```

---

# 📂 Project Structure

```
CampusOS/

├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
│
├── backend/
│   ├── agents/
│   ├── api/
│   ├── rag/
│   ├── database/
│   ├── uploads/
│   ├── app.py
│   ├── requirements.txt
│   └── .env.example
│
├── docs/
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

# 🛠️ Tech Stack

## Frontend
- React.js
- Tailwind CSS
- React Router
- Axios

## Backend
- FastAPI
- Python

## AI & LLM
- LangGraph
- LangChain
- Gemini / OpenAI / Groq
- Sentence Transformers

## RAG
- FAISS / ChromaDB

## Database
- PostgreSQL

## Authentication
- JWT Authentication

---

# 🔄 Workflow

```
User Request
      │
      ▼
Supervisor Agent
      │
      ▼
Select Appropriate AI Agent
      │
      ▼
LLM Processing
      │
      ▼
Response to User
```

---

# 📌 Current Implementation (Phase 1)

- ✅ Project Setup
- ✅ Full-Stack Architecture
- ✅ Multi-Agent Design
- ✅ Syllabus Chat Agent
- ✅ Assignment Assistant
- ✅ Resume Builder
- ✅ Timetable Generator

---

# 🚧 Future Scope

The complete CampusOS will include:

- AI Teacher
- Attendance Prediction
- AI Plagiarism Checker
- Smart Notice Board
- Placement Recommendation
- Student Analytics
- Faculty Dashboard
- Admin Dashboard
- Event Management
- Career Guidance Agent
- Voice Assistant
- OCR Integration

---

# ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/CampusOS.git
```

### Navigate to Project

```bash
cd CampusOS
```

### Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

# 👥 Team Members

| Role | Responsibility |
|------|----------------|
| AI Engineer | Multi-Agent System, LangGraph, RAG |
| Frontend Developer | React UI & Dashboard |
| Backend Developer | FastAPI, APIs, Database |
| AI Engineer | Resume Agent & Timetable Agent |

---

# 🎯 Project Goals

- Build a scalable AI-powered Campus Operating System
- Implement a modular Multi-Agent Architecture
- Demonstrate Retrieval-Augmented Generation (RAG)
- Showcase Full-Stack AI application development
- Improve students' academic productivity through intelligent automation

---

# 📜 License

This project is developed for educational and research purposes.

---

⭐ If you find this project useful, consider giving it a star!