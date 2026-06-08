from app.providers.openai_compatible import OpenAICompatibleProvider
from app.config.settings import settings

class OpenRouterProvider(OpenAICompatibleProvider):
    def __init__(self):
        super().__init__(
            name="openrouter",
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            default_model="meta-llama/llama-3.1-8b-instruct"
        )
