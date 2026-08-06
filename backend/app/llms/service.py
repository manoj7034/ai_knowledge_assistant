from app.llms.factory import LLMProviderFactory


class LLMService:

    def __init__(self):

        self.provider = (
            LLMProviderFactory.get_provider()
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        return self.provider.generate(prompt)