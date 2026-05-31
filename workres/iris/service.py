import os

import joblib
import pandas as pd

from features import decode_predictions

MODEL_PATH = os.getenv("MODEL_PATH", "model.joblib")


artifact_loaded = joblib.load(MODEL_PATH)
MODEL = artifact_loaded["model"] if isinstance(artifact_loaded, dict) else artifact_loaded


def calculate_result(features: dict[str, list[float]]) -> list[str]:
    df = pd.DataFrame(features)
    predictions = MODEL.predict(df).tolist()
    return decode_predictions(predictions)
