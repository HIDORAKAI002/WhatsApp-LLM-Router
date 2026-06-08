from app.providers.openai_compatible import OpenAICompatibleProvider
from app.config.settings import settings

class TogetherProvider(OpenAICompatibleProvider):
    def __init__(self):
        super().__init__(
            name="together",
            api_key=settings.TOGETHER_API_KEY,
            base_url="https://api.together.xyz/v1",
            default_model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
        )
