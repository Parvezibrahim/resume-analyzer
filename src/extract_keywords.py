from sklearn.feature_extraction.text import TfidfVectorizer
import re

def clean_text(text):
    return re.sub(r'[^a-zA-Z\s]', '', text.lower())

def extract_keywords(text, top_n=20):
    cleaned = clean_text(text)
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([cleaned])
    scores = zip(vectorizer.get_feature_names_out(), tfidf_matrix.toarray()[0])
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return [word for word, score in sorted_scores[:top_n]]

def extract_keywords_from_text(text, top_n=20):
    return extract_keywords(text, top_n)
