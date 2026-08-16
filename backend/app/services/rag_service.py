from app.llms.base import LLMProvider
from app.rag.context_builder import ContextBuilder
from app.rag.prompt_builder import RAGPromptBuilder


class RAGService:

    def __init__(
        self,
        llm: LLMProvider,
        context_builder: ContextBuilder,
        prompt_builder: RAGPromptBuilder,
    ):
        self.llm = llm
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder

    def generate_answer(
        self,
        *,
        query: str,
        documents: list[dict],
    ) -> str:

        context = self.context_builder.build(
            documents,
        )

        if not context:
            return (
                "I don't have enough information "
                "in the available documents to answer "
                "this question."
            )

        prompt = self.prompt_builder.build(
            query=query,
            context=context,
        )

        return self.llm.generate(prompt)