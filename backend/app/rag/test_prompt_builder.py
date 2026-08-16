from app.rag.prompt_builder import RAGPromptBuilder


def main():

    context = """
[Source 1]
File: Python_Interview.pdf
Chunk: 0

FastAPI is a modern Python web framework.

[Source 2]
File: FastAPI_Guide.pdf
Chunk: 2

Dependency Injection allows dependencies
to be provided automatically.
"""

    builder = RAGPromptBuilder()

    prompt = builder.build(
        query="What is FastAPI?",
        context=context,
    )

    print("\n========== RAG PROMPT ==========\n")
    print(prompt)


if __name__ == "__main__":
    main()