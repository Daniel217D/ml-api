class TestModelService:
    model_name = "test model"

    def predict(self, model_input: str) -> str:
        if not model_input.strip():
            return "test output"
        return "test output"


test_model_service = TestModelService()
