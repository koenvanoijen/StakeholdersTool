from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def cosine(text, query):
    vectorizer = TfidfVectorizer()
    query_vec = vectorizer.fit_transform(query)
    text_vec = vectorizer.transform([text])

    # Calculate cosine similarity
    similarity_score = cosine_similarity(query_vec, text_vec)[0][0]
    print(similarity_score)