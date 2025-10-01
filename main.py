import streamlit as st
import docx2txt
import PyPDF2
from sentence_transformers import SentenceTransformer, util

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
    st.write("Upload a Resume and provide a Job Description to compute a smart match score.")

    # Upload Resume
    uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    jd_text = st.text_area("Paste Job Description here")

    if uploaded_file and jd_text.strip():
        # Extract resume text
        if uploaded_file.type == "application/pdf":
            resume_text = read_pdf(uploaded_file)
        else:
            resume_text = read_docx(uploaded_file)

        if not resume_text.strip():
            st.error("Could not extract text from resume. Try another file.")
            return

        # Scores
        keyword_score = keyword_match_score(resume_text, jd_text)
        semantic_score = semantic_similarity(jd_text, resume_text)
        final_score = round(0.7 * semantic_score + 0.3 * keyword_score, 2)

        # Display results
        st.subheader("📊 Screening Results")
        st.write(f"**Keyword Match Score:** {keyword_score}%")
        st.write(f"**Semantic Match Score:** {semantic_score}%")
        st.success(f"✅ Final Candidate Match Score: {final_score}%")

        # Highlight keywords
        matched_keywords = set(resume_text.lower().split()).intersection(set(jd_text.lower().split()))
        if matched_keywords:
            st.subheader("🔍 Matched Keywords")
            st.write(", ".join(matched_keywords))

if __name__ == "__main__":
    main()
