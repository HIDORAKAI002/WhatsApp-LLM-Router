from app.providers.openai_compatible import OpenAICompatibleProvider
from app.config.settings import settings

class CerebrasProvider(OpenAICompatibleProvider):
    def __init__(self):
        super().__init__(
            name="cerebras",
            api_key=settings.CEREBRAS_API_KEY,
            base_url="https://api.cerebras.ai/v1",
            default_model="llama3.1-8b"
        )
