import logging
from app.config.settings import settings
from app.providers.groq import GroqProvider
from app.providers.openrouter import OpenRouterProvider
from app.providers.cerebras import CerebrasProvider
from app.providers.together_ai import TogetherProvider
# (Add other providers here as needed)

class LLMRouter:
    def __init__(self):
        self.providers = {}
        
        # Initialize available providers
        all_providers = [
            GroqProvider(),
            OpenRouterProvider(),
            CerebrasProvider(),
            TogetherProvider()
        ]
        
        for p in all_providers:
            if p.api_key:
                self.providers[p.provider_name] = p
                logging.info(f"Loaded provider: {p.provider_name}")

    async def call_llm(self, messages: list, tools: list = None) -> any:
        for provider_name in settings.FALLBACK_ORDER:
            provider = self.providers.get(provider_name.strip())
            if not provider:
                continue
                
            try:
                logging.info(f"Attempting inference with {provider_name}...")
                response = await provider.generate_response(messages, tools)
                return response
            except Exception as e:
                logging.warning(f"Provider {provider_name} failed: {e}. Falling back...")
                continue
                
        raise Exception("All fallback AI providers failed!")

llm_router = LLMRouter()
