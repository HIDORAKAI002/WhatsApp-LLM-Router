import os
from dotenv import load_dotenv

# Load env variables from the root folder
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

class Settings:
    TEXT_AGENT_URL: str = os.getenv("TEXT_AGENT_URL", "http://localhost:3000")
    FALLBACK_ORDER: list = os.getenv("AI_FALLBACK_ORDER", "groq,mistral,gemini").split(",")
    
    # Primary API Keys
    GROQ_API_KEYS: list = os.getenv("GROQ_API_KEYS", "").split(",")
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Open-Source & Custom API Keys
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    TOGETHER_API_KEY: str = os.getenv("TOGETHER_API_KEY", "")
    FIREWORKS_API_KEY: str = os.getenv("FIREWORKS_API_KEY", "")
    CEREBRAS_API_KEY: str = os.getenv("CEREBRAS_API_KEY", "")
    SAMBANOVA_API_KEY: str = os.getenv("SAMBANOVA_API_KEY", "")

settings = Settings()
