from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from app.utils import preprocess_text, clean_text, process_text
import joblib, os

# Setting the Minimum Similarity Threshold
MIN_SIMILARITY_THRESHOLD = int(os.environ.get("MIN_SIMILARITY_THRESHOLD"))

# Function to compute the cosine similarity check using k-NN ML algorithm
def cosine_similarity_with_knn(experience_description):
    # Initialize the vectorizer
    vectorizer = joblib.load("vectorizer.pkl")

    # Initialize the model
    model = joblib.load("knn-model.pkl")

    # Initialize the data
    new_df = joblib.load("data.pkl")

    cleaned_experience = process_text(experience_description)
    query_vector = vectorizer.transform([cleaned_experience])
    distances, indices = model.kneighbors(query_vector)

    if len(cleaned_experience.split()) < 10:
        return "Please provide a more detailed work experience for better recommendations."

    recommendations = []
    for i, index in enumerate(indices[0]):
        similarity = (1 - distances[0][i]) * 100
        
        if similarity < MIN_SIMILARITY_THRESHOLD:
            continue
        
        unit_code = new_df.iloc[index]['code']  
        unit_name = new_df.iloc[index]['name']
        
        recommendations.append((unit_code, unit_name, round(similarity, 2)))

    return recommendations


def compute_model(description):
    # Initialize the models
    trained_models = joblib.load("trained_models.pkl")

    # Initialize the unit outcomes vector
    X_tfidf = joblib.load("X_tfidf.pkl")

    # Initialize the vectorizer
    tfidf_vectorizer = joblib.load("tfidf_vectorizer.pkl")

    # Preprocess the student's input
    cleaned_input = preprocess_text(description)

    # Vectorize the applicant's experience description
    input_vector = tfidf_vectorizer.transform([cleaned_input])

    # Function to get recommendations and their match percentages for a model
    # recommendations = {}

    # Initialize a list to collect recommended units
    recommended_units = []

    # Iterate through models to get the recommendations
    for model_name, model in trained_models.items():
        recommendation = model.predict(input_vector)[0]
        recommended_units.append(recommendation)

    return recommended_units
