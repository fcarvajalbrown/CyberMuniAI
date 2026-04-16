from strands.models.ollama import OllamaModel

MODEL_ID = "ministral-3:3b"
OLLAMA_HOST = "http://localhost:11434"

def get_model() -> OllamaModel:
    return OllamaModel(
        model_id=MODEL_ID,
        host=OLLAMA_HOST,
        keep_alive="30m",  # keep model hot between queries
        options={"num_ctx": 4096},
    )