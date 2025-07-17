import numpy as np
from joblib import load

model = load("src/ml/model.joblib")
category_encoder = load("src/ml/category_encoder.joblib")


def predict_stars(input_data: dict) -> int:
    try:
        price = float(input_data["price"])
        category = input_data["category"].lower()

        if category not in category_encoder.classes_:
            raise ValueError(f"Category '{category}' not recognized.")

        category_encoded = category_encoder.transform([category])[0]

        features = np.array([[price, category_encoded]])

        predicted_stars = model.predict(features)[0]
        return int(predicted_stars)

    except Exception as e:
        raise ValueError(f"Error on prediction: {e}")
