from app.config.settings import settings
from app.llms.base import LLMProvider
from app.llms.gemini import GeminiProvider
from app.llms.ollama import OllamaProvider


class LLMProviderFactory:

    @staticmethod
    def get_provider() -> LLMProvider:

        if settings.LLM_PROVIDER == "gemini":
            return GeminiProvider()

        if settings.LLM_PROVIDER == "ollama":
            return OllamaProvider(
                settings.LLM_MODEL,
            )

        raise ValueError(
            f"Unsupported LLM provider: {settings.LLM_PROVIDER}"
        )