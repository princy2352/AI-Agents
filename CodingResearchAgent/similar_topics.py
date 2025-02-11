from sentence_transformers import SentenceTransformer, util

# Initialize model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Predefined topics for suggestions
coding_topics = [
    "Machine Learning", "Deep Learning", "Data Science",
    "Web Development", "Computer Vision",
    "Natural Language Processing", "Reinforcement Learning"
]

# Function to find similar topics
def get_similar_topics(user_query):
    query_embedding = model.encode(user_query, convert_to_tensor=True)
    topic_embeddings = model.encode(coding_topics, convert_to_tensor=True)

    # Compute cosine similarity
    cosine_scores = util.pytorch_cos_sim(query_embedding, topic_embeddings)
    similar_topics = sorted(zip(coding_topics, cosine_scores[0].tolist()), key=lambda x: x[1], reverse=True)

    # Return top 3 similar topics
    return [topic for topic, score in similar_topics[:3] if score > 0.4]  # Adjust threshold as needed
