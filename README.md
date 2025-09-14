# AI-Powered Resume Screener

An AI tool to parse resumes (PDF/DOCX) and match them with job descriptions using NLP.

## 🚀 Features
- Parse PDF/DOCX resumes
- Extract job description keywords
- Match candidate skills with job requirements
- Display match score and missing keywords

## 📂 Project Structure
- `app/` → parsers & matcher logic
- `main.py` → Streamlit frontend
- `data/` → sample resumes and job descriptions
- `results/` → match reports

## ⚙️ Setup
```bash
git clone https://github.com/yourusername/AI-Resume-Screener.git
cd AI-Resume-Screener
pip install -r requirements.txt
streamlit run main.py

🎯 Output

Match Score (%) between resume and JD

List of Matched Skills

Missing Skills (gaps for the candidate)
