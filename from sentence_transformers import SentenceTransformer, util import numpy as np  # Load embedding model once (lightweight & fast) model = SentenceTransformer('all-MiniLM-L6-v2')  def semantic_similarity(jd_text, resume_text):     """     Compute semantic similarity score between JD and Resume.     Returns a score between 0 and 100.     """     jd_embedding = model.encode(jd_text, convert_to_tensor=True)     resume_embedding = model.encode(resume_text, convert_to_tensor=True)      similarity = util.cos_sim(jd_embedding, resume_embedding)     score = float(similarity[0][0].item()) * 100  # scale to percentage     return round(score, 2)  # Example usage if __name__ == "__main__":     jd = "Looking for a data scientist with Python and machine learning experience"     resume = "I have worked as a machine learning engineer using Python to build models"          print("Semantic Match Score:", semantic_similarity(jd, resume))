from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load embedding model once (lightweight & fast)
model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_similarity(jd_text, resume_text):
    """
    Compute semantic similarity score between JD and Resume.
    Returns a score between 0 and 100.
    """
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    similarity = util.cos_sim(jd_embedding, resume_embedding)
    score = float(similarity[0][0].item()) * 100  # scale to percentage
    return round(score, 2)

# Example usage
if __name__ == "__main__":
    jd = "Looking for a data scientist with Python and machine learning experience"
    resume = "I have worked as a machine learning engineer using Python to build models"
    
    print("Semantic Match Score:", semantic_similarity(jd, resume))
