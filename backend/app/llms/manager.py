from app.llms.base import LLMProvider
from app.llms.factory import LLMProviderFactory


_llm: LLMProvider | None = None


def initialize_llm() -> None:
    global _llm

    if _llm is None:
        print("Loading LLM...")
        _llm = LLMProviderFactory.get_provider()
        print("LLM ready.")


def get_llm() -> LLMProvider:
    if _llm is None:
        raise RuntimeError(
            "LLM has not been initialized."
        )

    return _llm


def shutdown_llm() -> None:
    global _llm
    _llm = None