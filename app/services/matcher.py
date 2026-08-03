from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# We are using 'all-MiniLM-L6-v2'. It is highly optimized, fast, and excellent for semantic matching.
# The first time this runs, it will download the lightweight model weights.
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_match_score(resume_text: str, jd_text: str) -> float:
    """
    Converts both the resume and the job description into vector embeddings,
    then calculates the cosine similarity to return a match score (0-100%).
    """
    if not resume_text or not jd_text:
        return 0.0
    
    # 1. Convert text to embeddings
    embeddings = model.encode([resume_text, jd_text])
    
    # 2. Calculate Cosine Similarity between Resume (index 0) and JD (index 1)
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    
    # 3. Convert to a percentage and round it
    score = round(float(similarity) * 100, 2)
    
    # Prevent negative scores in edge cases
    return max(0.0, score)