# 🚀 AI Resume Matcher & Learning Roadmap Generator

An intelligent, full-stack NLP platform designed to bridge the gap between job requirements and applicant skills. This application accepts a resume (PDF) and a target Job Description, processes the text using advanced Natural Language Processing (NLP), and outputs a highly accurate Match Percentage along with a dynamically generated learning roadmap.

**🔗 [Live Demo - Try it here!](https://resume-analyzer-frontend-gold.vercel.app/)** **🔗 [Backend API URL](https://resume-analyzer-backend-api-cmzw.onrender.com)**

---

## ✨ Key Features

* **Intelligent Document Parsing:** Extracts raw text from standard PDFs and utilizes Tesseract-OCR for image-based or scanned documents.
* **NLP Skill Extraction:** Powered by `spaCy` (`en_core_web_sm`) to tokenize, lemmatize, and isolate technical engineering keywords.
* **Cosine Similarity Scoring:** Uses `scikit-learn` (TF-IDF Vectorizer) to mathematically calculate the semantic alignment between a resume and a job description.
* **Automated Gap Analysis:** Accurately identifies "Missing Skills" that the candidate lacks for the specified role.
* **Dynamic Learning Roadmaps:** Maps missing skills to a proprietary database of ~1,800 skills, providing custom Open-Access research papers, YouTube playlists, and MOOCs.
* **Custom 5-Tier Scraper Architecture:** The backend database was populated using a custom data pipeline cascading through the OpenAlex API, arXiv API, DEV.to, and GeeksforGeeks to secure university-grade educational material.

---

## 🛠️ Tech Stack

### Frontend (Deployed on Vercel)
* **Framework:** React.js / Next.js
* **Styling:** Tailwind CSS
* **API Integration:** Fetch/Axios for secure cross-origin requests.

### Backend & AI (Deployed on Render via Docker)
* **Core:** Python 3.10, Flask, Gunicorn
* **NLP & ML:** spaCy, scikit-learn
* **PDF & OCR:** PyMuPDF (fitz), pdf2image, Poppler, pytesseract
* **Data Storage:** Highly curated Local JSON Database 

---

## 💻 Local Setup & Installation

If you want to run this project locally, follow these steps:

**1. Clone the repository**
`git clone https://github.com/Code-with-Prabhjot/resume-analyzer-backend.git`
`cd resume-analyzer-backend`

**2. Create a virtual environment**
`python -m venv venv`
`source venv/bin/activate`

**3. Install dependencies**
`pip install -r requirements.txt`
`python -m spacy download en_core_web_sm`

**4. Run the Flask Server**
`python app.py`

---

## 👥 Contributors

* **Prabhjot Singh** - Core System Architecture, AI/NLP Engine & Backend Logic
* **Manleen Kaur** - Frontend Architecture, UI/UX Design & Client Integration
* **Hamsika Challa** - Auxiliary Python Scripting & Domain Data Curation
