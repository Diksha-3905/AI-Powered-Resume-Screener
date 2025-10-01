import streamlit as st
import docx2txt
import PyPDF2
from sentence_transformers import SentenceTransformer, util
import pandas as pd

# -------------------------------
# Load embedding model once
# -------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------------
# Helpers: resume parsing
# -------------------------------
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def read_docx(file):
    return docx2txt.process(file)

def extract_resume_text(file):
    if file.type == "application/pdf":
        return read_pdf(file)
    else:
        return read_docx(file)

# -------------------------------
# Keyword-based matching
# -------------------------------
def keyword_match_score(resume_text, jd_text):
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())
    
    matched = resume_words.intersection(jd_words)
    if not jd_words:
        return 0
    return round((len(matched) / len(jd_words)) * 100, 2)

# -------------------------------
# Semantic similarity
# -------------------------------
def semantic_similarity(jd_text, resume_text):
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    
    similarity = util.cos_sim(jd_embedding, resume_embedding)
    score = float(similarity[0][0].item()) * 100
    return round(score, 2)

# -------------------------------
# Streamlit App
# -------------------------------
def main():
    st.title("AI-Powered Resume Screener 📄🤖")
    st.write("Upload one or more resumes and provide a Job Description to compute match scores.")

    # Upload multiple resumes
    uploaded_files = st.file_uploader("Upload Resumes (PDF/DOCX)", type=["pdf", "docx"], accept_multiple_files=True)
    jd_text = st.text_area("Paste Job Description here")

    if uploaded_files and jd_text.strip():
        results = []

        for file in uploaded_files:
            resume_text = extract_resume_text(file)

            if not resume_text.strip():
                continue

            keyword_score = keyword_match_score(resume_text, jd_text)
            semantic_score = semantic_similarity(jd_text, resume_text)
            final_score = round(0.7 * semantic_score + 0.3 * keyword_score, 2)

            results.append({
                "Candidate": file.name,
                "Keyword Score (%)": keyword_score,
                "Semantic Score (%)": semantic_score,
                "Final Score (%)": final_score
            })

        if results:
            df = pd.DataFrame(results).sort_values(by="Final Score (%)", ascending=False)
            st.subheader("📊 Candidate Ranking")
            st.dataframe(df, use_container_width=True)

            # Download option
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Results as CSV", data=csv, file_name="resume_ranking.csv", mime="text/csv")

            top_candidate = df.iloc[0]
            st.success(f"🏆 Top Candidate: {top_candidate['Candidate']} ({top_candidate['Final Score (%)']}%)")

if __name__ == "__main__":
    main()
