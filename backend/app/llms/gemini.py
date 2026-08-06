from google import genai

from app.config.settings import settings
from app.llms.base import LLMProvider


class GeminiProvider(LLMProvider):

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

    def generate(self, prompt: str,) -> str:

        response = self.client.models.generate_content(
            model=settings.LLM_MODEL,
            contents=prompt,
        )

        return response.text # type: ignore