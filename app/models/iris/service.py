from pathlib import Path

import joblib
import pandas as pd
from .artifacts import features as iris_features


class ModelService:
    model_name = "iris dataset model"

    def __init__(self) -> None:
        artifacts_dir = Path(__file__).resolve().parent / "artifacts"
        self._model = joblib.load(artifacts_dir / "model.joblib")['model']

    def predict(
        self,
        *,
        sepal_length_cm: float,
        sepal_width_cm: float,
        petal_length_cm: float,
        petal_width_cm: float,
    ) -> str:
        features = pd.DataFrame(
            [
                {
                    "sepal length (cm)": sepal_length_cm,
                    "sepal width (cm)": sepal_width_cm,
                    "petal length (cm)": petal_length_cm,
                    "petal width (cm)": petal_width_cm,
                }
            ]
        )
        prediction = self._model.predict(features)[0]
        return self.target_names.get(int(prediction), str(prediction))
