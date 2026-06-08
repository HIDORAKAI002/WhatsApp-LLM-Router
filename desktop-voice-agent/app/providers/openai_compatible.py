from app.providers.base_provider import BaseProvider
from openai import AsyncOpenAI
import logging

class OpenAICompatibleProvider(BaseProvider):
    def __init__(self, name: str, api_key: str, base_url: str, default_model: str):
        self._name = name
        self.api_key = api_key
        self.base_url = base_url
        self.default_model = default_model
        
        if self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            self.client = None

    @property
    def provider_name(self) -> str:
        return self._name

    async def generate_response(self, messages: list, tools: list = None) -> any:
        if not self.client:
            raise ValueError(f"API Key for {self.provider_name} is missing.")
            
        kwargs = {
            "model": self.default_model,
            "messages": messages,
            "max_tokens": 200
        }
        
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
            
        try:
            response = await self.client.chat.completions.create(**kwargs)
            return response
        except Exception as e:
            logging.error(f"Error in provider {self.provider_name}: {e}")
            raise e
