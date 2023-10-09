from sklearn.metrics.pairwise import cosine_similarity
from app.utils import preprocess_text
import joblib


# Function to compute the cosine similarity check
def cosine_similarity_check(experience_description):
    # Initialize the unit outcomes vector
    X_tfidf = joblib.load("X_tfidf.pkl")

    # Initialize the vectorizer
    tfidf_vectorizer = joblib.load("tfidf_vectorizer.pkl")

    # Preprocess the student's input
    cleaned_input = preprocess_text(experience_description)

    # Vectorize the applicant's experience description
    input_vector = tfidf_vectorizer.transform([cleaned_input])

    cosine_similarities = cosine_similarity(input_vector, X_tfidf)

    # Set a similarity threshold
    similarity_threshold = 0.2

    # Initialize a list to collect recommended units
    recommended_units = []

    # Check if the highest similarity is above the threshold
    if cosine_similarities.max() >= similarity_threshold:
        recommended_unit_index = cosine_similarities.argmax()
        recommended_unit = X_tfidf.unit_names[recommended_unit_index]
        recommended_units.append(recommended_unit)

    return recommended_units


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
