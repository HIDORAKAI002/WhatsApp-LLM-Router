import random
from app.providers.openai_compatible import OpenAICompatibleProvider
from app.config.settings import settings

class GroqProvider(OpenAICompatibleProvider):
    def __init__(self):
        # Handle multiple keys for load balancing safely
        valid_keys = [k for k in settings.GROQ_API_KEYS if k.strip()]
        key = random.choice(valid_keys) if valid_keys else ""
        
        super().__init__(
            name="groq",
            api_key=key,
            base_url="https://api.groq.com/openai/v1",
            default_model="llama-3.1-8b-instant"
        )
