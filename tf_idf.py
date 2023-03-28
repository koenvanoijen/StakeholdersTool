from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def cosine(text, query):
    """ text as one sentence and queries as seperate words"""
    # Convert text and search queries to feature vectors
    vectorizer = TfidfVectorizer()

    query_vec = vectorizer.fit_transform([text])
    text_vec = vectorizer.transform(query)

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(query_vec, text_vec)
    print()
    print("similarity score: ", similarity_scores)

    return similarity_scores[0]


def scoreAnalysis(similarity_scores, weights):
    # Different kind of analyses are possible. Depending on what is most convenient

    # return sum(similarity_scores)/len(similarity_scores)
    # return max(similarity_scores)
    return sum(weights*similarity_scores)


# count the occurrences of the words and weight them with the size of the text
def occurranceMatching(text, queries):
    """ text as seperate and queries as seperate words"""
    query_freq = {}
    search_query_words= [query.split() for query in queries]
    for query in search_query_words:
        freq = sum([text.count(word) for word in query])
        print(freq)
        query_freq[' '.join(query)] = freq / len(text)

    # Rank search queries by relevance
    ranked_queries = sorted(query_freq.items(), key=lambda x: x[1], reverse=True)
    # Display results
    for query, score in ranked_queries:
       print(f"{query}: {score}")
