from fastapi import FastAPI, UploadFile, File
from typing import List
import fitz
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import re

app = FastAPI()

print("Loading ML model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded!")

# Common tech skills dictionary for keyword matching
TECH_SKILLS = [
    # Languages
    "python", "java", "javascript", "sql", "r", "scala", "c++",
    # ML/AI
    "machine learning", "deep learning", "nlp", "computer vision",
    "neural networks", "reinforcement learning", "transfer learning",
    # Libraries
    "scikit-learn", "tensorflow", "keras", "pytorch", "pandas",
    "numpy", "matplotlib", "seaborn", "plotly", "opencv",
    # GenAI
    "langchain", "faiss", "huggingface", "transformers", "rag",
    "llm", "gpt", "bert", "llama", "prompt engineering",
    # MLOps
    "mlflow", "docker", "kubernetes", "airflow", "fastapi",
    "flask", "streamlit", "rest api", "microservices",
    # Data
    "sql", "mysql", "postgresql", "mongodb", "spark", "hadoop",
    "data analysis", "data visualization", "eda", "feature engineering",
    "statistical analysis", "predictive modeling",
    # Cloud
    "aws", "azure", "gcp", "cloud computing",
    # Tools
    "git", "github", "jupyter", "postman", "spring boot"
]

def extract_text(file_bytes, filename=""):
    if filename.endswith('.txt'):
        return file_bytes.decode('utf-8')
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def extract_keywords(text):
    text_lower = text.lower()
    found = []
    for skill in TECH_SKILLS:
        if skill in text_lower:
            found.append(skill)
    return found

def compute_similarity(jd_text, resume_texts):
    all_texts = [jd_text] + resume_texts
    embeddings = model.encode(all_texts, normalize_embeddings=True)
    jd_embedding = embeddings[0].reshape(1, -1).astype('float32')
    resume_embeddings = embeddings[1:].astype('float32')
    dimension = jd_embedding.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(resume_embeddings)
    scores, indices = index.search(jd_embedding, len(resume_texts))
    return scores[0], indices[0]

def analyze_resume(jd_keywords, resume_text, resume_keywords):
    # Matched keywords
    matched = [k for k in jd_keywords if k in resume_keywords]

    # Missing keywords
    missing = [k for k in jd_keywords if k not in resume_keywords]

    # Extra skills candidate has beyond JD
    extra = [k for k in resume_keywords if k not in jd_keywords]

    # Keyword match percentage
    keyword_match = round(
        len(matched) / len(jd_keywords) * 100
        if jd_keywords else 0, 1
    )

    # Strengths — top matched skills
    strengths = matched[:5] if matched else ["No matching skills found"]

    # Weaknesses — top missing skills
    weaknesses = missing[:5] if missing else ["All key skills present"]

    return {
        "matched_keywords": matched,
        "missing_keywords": missing,
        "extra_skills": extra,
        "keyword_match_percent": keyword_match,
        "strengths": strengths,
        "skills_gap": weaknesses
    }

@app.post("/screen")
async def screen_resumes(
    jd: UploadFile = File(...),
    resumes: List[UploadFile] = File(...)
):
    # Extract JD
    jd_bytes = await jd.read()
    jd_text = extract_text(jd_bytes, jd.filename)

    if not jd_text:
        return {"error": "Could not extract text from JD"}

    # Extract JD keywords
    jd_keywords = extract_keywords(jd_text)

    # Extract resume texts
    resume_texts = []
    resume_names = []
    resume_keywords_list = []

    for resume in resumes:
        resume_bytes = await resume.read()
        text = extract_text(resume_bytes, resume.filename)
        if text:
            resume_texts.append(text)
            resume_names.append(resume.filename)
            resume_keywords_list.append(extract_keywords(text))

    if not resume_texts:
        return {"error": "Could not extract text from resumes"}

    # Compute similarity scores
    scores, indices = compute_similarity(jd_text, resume_texts)

    # Build ranked results with analysis
    results = []
    for rank, (score, idx) in enumerate(zip(scores, indices)):
        idx = int(idx)
        analysis = analyze_resume(
            jd_keywords,
            resume_texts[idx],
            resume_keywords_list[idx]
        )
        results.append({
            "rank": rank + 1,
            "filename": resume_names[idx],
            "match_score": round(float(score) * 100, 2),
            "keyword_match_percent": analysis["keyword_match_percent"],
            "matched_keywords": analysis["matched_keywords"],
            "missing_keywords": analysis["missing_keywords"],
            "extra_skills": analysis["extra_skills"],
            "strengths": analysis["strengths"],
            "skills_gap": analysis["skills_gap"]
        })

    return {
        "total_resumes": len(resume_texts),
        "jd_file": jd.filename,
        "jd_keywords_found": jd_keywords,
        "ranked_candidates": results
    }

@app.get("/health")
def health():
    return {"status": "ML service is running!"}