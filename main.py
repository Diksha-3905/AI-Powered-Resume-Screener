import streamlit as st
from app.parser import extract_resume_text
from app.jd_parser import extract_jd_keywords
from app.matcher import match_resume_with_jd

st.title("AI-Powered Resume Screener")
st.write("Upload a resume and job description to check match score.")

resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
jd_text = st.text_area("Paste Job Description Here")

if resume_file and jd_text:
    with open("temp_resume." + resume_file.name.split(".")[-1], "wb") as f:
        f.write(resume_file.getbuffer())

    resume_text = extract_resume_text(f.name)
    jd_keywords = extract_jd_keywords(jd_text)
    result = match_resume_with_jd(resume_text, jd_keywords)

    st.subheader("Match Report")
    st.write(f"**Match Score:** {result['match_score']}%")
    st.write("**Matched Keywords:**", result["matched_keywords"])
    st.write("**Missing Keywords:**", result["missing_keywords"])
