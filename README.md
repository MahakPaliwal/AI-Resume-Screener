# 🤖 AI-Powered Resume Screener

An intelligent full-stack application that ranks candidates by analyzing 
their resumes against a Job Description using semantic similarity and 
keyword matching.

---

## ✨ Features

- **Semantic Matching** — Ranks resumes by meaning using Sentence Transformers
- **Keyword Matching** — Shows which JD keywords are present in each resume
- **Skills Gap Analysis** — Identifies missing skills per candidate
- **Additional Skills** — Highlights extra skills candidate brings beyond JD
- **Dual JD Input** — Upload PDF or paste JD text directly
- **Multiple Resume Upload** — Analyze multiple candidates at once
- **Visual Dashboard** — Clean UI with progress bars and color-coded tags

---

## 🏗️ Architecture
Frontend (HTML/CSS/JS)
↓
Java Spring Boot (REST API) — Port 8080
↓
Python FastAPI (ML Service) — Port 8000
↓
Sentence Transformers + FAISS
---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Java, Spring Boot |
| ML Service | Python, FastAPI |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Vector Search | FAISS |
| PDF Parsing | PyMuPDF |

---

## 📊 Sample Output

- **Semantic Match Score** — Overall resume relevance to JD
- **Keyword Match %** — Percentage of JD keywords found in resume
- **Matched Keywords** — Skills present in both JD and resume
- **Skills Gap** — JD keywords missing from resume
- **Additional Skills** — Extra skills candidate has beyond JD requirements

---

## 🚀 How to Run

### Prerequisites
- Java 17+
- Python 3.8+
- Maven

### Step 1 — Clone the repo
```bash
git clone https://github.com/MahakPaliwal/ai-resume-screener.git
cd ai-resume-screener
```

### Step 2 — Start ML Service
```bash
cd ml-service
pip install fastapi uvicorn sentence-transformers faiss-cpu pymupdf python-multipart
python -m uvicorn main:app --reload --port 8000
```

### Step 3 — Start Spring Boot
```bash
cd resume-screener
.\mvnw.cmd spring-boot:run   # Windows
./mvnw spring-boot:run       # Mac/Linux
```

### Step 4 — Open Frontend
Open `frontend/index.html` in your browser or use Live Server.

### Step 5 — Use the app
1. Upload a Job Description PDF or paste JD text
2. Upload one or more resume PDFs
3. Click **"Screen Resumes"**
4. See ranked candidates with detailed analysis

---

## 📁 Project Structure
ai-resume-screener/
├── resume-screener/          ← Spring Boot backend
│   ├── src/
│   │   └── main/java/com/resumescreener/
│   │       ├── ResumeScreenerApplication.java
│   │       └── ScreenerController.java
│   └── pom.xml
├── ml-service/               ← Python ML service
│   └── main.py
├── frontend/                 ← UI
│   └── index.html
└── README.md
---

## 🔍 How It Works

1. **PDF Parsing** — PyMuPDF extracts text from uploaded PDFs
2. **Keyword Extraction** — Matches 50+ tech skills against JD and resumes
3. **Semantic Embedding** — Sentence Transformers converts text to vectors
4. **FAISS Search** — Finds most similar resumes to JD using cosine similarity
5. **Gap Analysis** — Compares JD keywords vs resume keywords
6. **Ranking** — Candidates ranked by semantic match score

---

## 👩‍💻 Built by

**Mahak Paliwal**

- 📧 mahakpaliwal58@gmail.com
- 🔗 [LinkedIn](https://linkedin.com/in/mahak-paliwal-a739841a1)
- 💻 [GitHub](https://github.com/MahakPaliwal)
![Demo]
<img width="1037" height="755" alt="image" src="https://github.com/user-attachments/assets/203eac0b-d09b-4789-a215-701f0d02c579" />

