class ModelService:
    model_name = "iris dataset model"

    def predict(self, model_input: str) -> str:
        return 'iris output: ' + model_input
