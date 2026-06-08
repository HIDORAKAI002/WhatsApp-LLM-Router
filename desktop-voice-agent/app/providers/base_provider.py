from abc import ABC, abstractmethod

class BaseProvider(ABC):
    """
    Abstract base class for all LLM providers in the Enterprise Architecture.
    """
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Returns the internal name of the provider."""
        pass
        
    @abstractmethod
    async def generate_response(self, messages: list, tools: list = None) -> any:
        """
        Sends the messages to the API provider and returns the raw response object.
        Must handle its own specific exceptions.
        """
        pass
